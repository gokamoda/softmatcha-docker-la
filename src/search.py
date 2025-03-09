#!/usr/bin/env python3
import json
import re
from argparse import Namespace
from collections import defaultdict
from typing import Any, TypeVar

import numpy as np
from softmatcha import configs, stopwatch
from softmatcha.cli.search_inverted_index import Statistics, search_texts
from softmatcha.search import Search, SearchIndex, SearchIndexInvertedFile
from softmatcha.struct import Pattern
from softmatcha.struct.index_inverted import IndexInvertedFileCollection

output_cfg = Namespace(
    json=True,
    profile=True,
    log=None,
    line_number=False,
    with_filename=False,
    no_filename=True,
    only_matching=False,
    quiet=False,
)


def get_formatted_search_result(
    pattern: str,
    tokenizer: Any,
    embedding: Any,
    threshold: float,
    indexes: IndexInvertedFileCollection,
    start_line: int = 0,
    max_lines: int = 250,
):
    stopwatch.timers.reset(profile=output_cfg.profile)
    pattern_tokens = tokenizer(pattern)
    pattern_embeddings = embedding(pattern_tokens)
    pattern = Pattern.build(
        pattern_tokens,
        pattern_embeddings,
        [threshold] * len(pattern_embeddings),
    )

    for file_path, file_index in zip(indexes.paths, indexes.indexes):
        searcher = SearchIndexInvertedFile(
            file_index, tokenizer, embedding, use_hash=True
        )

        result_htmls = []
        Statistics(0, 0)
        count = -1

        result_generator = search_texts(
            pattern,
            file_path,
            searcher,
            tokenizer,
            output_cfg=output_cfg,
            start_line=start_line,
        )
        try:
            for count, res in enumerate(result_generator):
                if count == 0:
                    return_dict = {
                        "total_hits": res.stats.num_hit_spans,
                        "search_time": stopwatch.timers.elapsed_time["search"],
                        "pattern_length": len(pattern),
                        "pattern_tokenized": tokenizer.decode(pattern_tokens),
                        "result_truncated": False,
                    }

                if count + 1 > max_lines:
                    return_dict["result_truncated"] = True
                    break

                result = json.loads(res.text)
                result_html = "<td>"

                current_position = 0
                for rb_begin, token, score in zip(
                    sum(result["matched_token_start_positions"], []),
                    sum(result["matched_tokens"], []),
                    sum(result["scores"], []),
                ):
                    result_html += (
                        result["original_line"][current_position:rb_begin]
                        + f" <ruby class='text-success'>{result['original_line'][rb_begin:rb_begin + len(token)]}<rt>{score:.2f}&nbsp;</rt></ruby> "
                    )
                    current_position = rb_begin + len(token)
                result_html += result["original_line"][current_position:] + "</td>"
                result_htmls.append(result_html)

                if count + 1 == max_lines:
                    return_dict["end_line"] = result["line_number"]
        except ValueError:
            "no result found"
            pass

        result_generator.close()

        if count == -1:
            return_dict = {
                "total_hits": 0,
                "search_time": stopwatch.timers.elapsed_time["search"],
                "pattern_length": len(pattern),
                "pattern_tokenized": tokenizer.decode(pattern_tokens),
                "result_truncated": False,
                "end_line": -1,
            }

        return_dict["html_lines"] = result_htmls

        return return_dict
