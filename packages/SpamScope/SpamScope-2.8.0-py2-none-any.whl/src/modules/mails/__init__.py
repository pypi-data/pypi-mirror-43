"""
Copyright 2017 Fedele Mantuano (https://www.linkedin.com/in/fmantuano/)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from .post_processing import processors, spamassassin
from .phishing import check_form, check_urls, check_phishing
from .spamassassin_analysis import (
    obj_report,
    report_from_file,
    analysis_from_file,
    report_from_string,
    convert_ascii2json)
from .dialects import (
    get_dialect_fingerprints,
    get_dialect_str,
    get_dialect,
    get_elastic_indices,
    get_messages_str,
    get_messages,
    make_dialect_report)
