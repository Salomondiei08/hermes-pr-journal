# 20 Target Repos for High-Value PRs

Generated: 2026-04-29 12:41:59 UTC

Ranked using live GitHub signals: recent merged PRs, recent closed-unmerged PRs, and contribution labels.

## 1. pytest-dev/pytest

- Activity score: 22.0
- Stars: 13814
- Good first issue: True
- Help wanted: False
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; maintenance work that aligns with existing tooling and CI conventions
- Avoid patterns: speculative feature work without prior alignment
- Opportunity areas: maintainer-tagged onboarding issues
- Signal labels: good first issue, plugin: debugging, status: help wanted, type: bug, type: enhancement
- Recent merged examples:
  - #14422 Fix duplicate values in Config.known_args_namespace for append actions (@EternalRights)
  - #14426 [pre-commit.ci] pre-commit autoupdate (@pre-commit-ci[bot])
  - #14419 [automated] Update plugin list (@github-actions[bot])
  - #14420 [PR #14391/cd7592c4 backport][9.0.x] Use direct cause for raises match failures (@patchback[bot])
  - #14421 changelog: fix up #14389 entry (@bluetech)
- Recent closed-unmerged examples:
  - #14428 .3493624936399236:b7404d45aa80f3721d9cf7a6f2e3d0e9_69f1ded19838cf54136eafe3.69f1dfad9838cf54136eafe6.69f1dfad6b3aba23f986e7ef:Trae CN.T(2026/4/29 18:38:37) (@muyusajiangtian)
  - #14424 testing: add regression test for get_user() swallowing OSError (#13835) (@OfekDanny)
  - #14358 Fix RaisesGroup calling check() on contained exceptions instead of Ex… (@kelliott1)
  - #14411 fix(raises): guard check callback against AttributeError in RaisesGroup diagnostic path (@armorbreak001)

## 2. encode/httpx

- Activity score: 21.0
- Stars: 15248
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; docs clarifications tied to real behavior or workflow pain; maintenance work that aligns with existing tooling and CI conventions
- Avoid patterns: generic docs rewrites not tied to a concrete confusion or bug; drive-by dependency or chore PRs unless explicitly requested
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; small scoped enhancements after issue-thread alignment
- Signal labels: bug, enhancement, good first issue, help wanted
- Recent merged examples:
  - #3773 Adapt test_response_decode_text_using_autodetect for chardet 6.0 (@musicinmybrain)
  - #3730 3.11+ (@lovelydinosaur)
  - #3699 Expose `FunctionAuth` in `__all__` (@thejcannon)
  - #3703 docs/ssl: fix typo (@xrmx)
  - #3692 Fixed a syntax error in the file upload example (@Zproger)
- Recent closed-unmerged examples:
  - #3241 Change default encoding to utf-8 in `normalize_header_key` and `normalize_header_value` functions (@SonderZhong)
  - #3762 Bump cryptography from 45.0.7 to 46.0.5 (@dependabot[bot])
  - #3765 docs: use canonical Requests docs URL (@droppingbeans)
  - #3759 Fix: Merge URL query parameters instead of replacing them (@veeceey)

## 3. jupyter/nbconvert

- Activity score: 21.0
- Stars: 1921
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; maintenance work that aligns with existing tooling and CI conventions; incremental features when they are narrow and clearly justified
- Avoid patterns: speculative feature work without prior alignment; drive-by dependency or chore PRs unless explicitly requested
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; small scoped enhancements after issue-thread alignment
- Signal labels: bug, documentation, enhancement, good first issue, help wanted
- Recent merged examples:
  - #2277 chore: update pre-commit hooks (@pre-commit-ci[bot])
  - #2276 specify python version for pre (@minrk)
  - #2242 chore: update pre-commit hooks (@pre-commit-ci[bot])
  - #2273 Bump the actions group across 1 directory with 2 updates (@dependabot[bot])
  - #2249 Tweak webpdf template logic to fix duplicate extension problem (@timkpaine)
- Recent closed-unmerged examples:
  - #2272 Bump actions/upload-artifact from 6 to 7 in the actions group (@dependabot[bot])
  - #1688 Set cm-unicode font for latex if available (fixes #1673) (@cgevans)
  - #1751 Add upper bound on the Jinja dependency and MarkupSafe (@martinRenou)
  - #842 Add --save-on-error flag, closes #626 (@ls1xt)

## 4. psf/black

- Activity score: 21.0
- Stars: 41491
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; docs clarifications tied to real behavior or workflow pain; maintenance work that aligns with existing tooling and CI conventions
- Avoid patterns: speculative feature work without prior alignment; generic docs rewrites not tied to a concrete confusion or bug
- Opportunity areas: maintainer-tagged onboarding issues
- Signal labels: good first issue, help wanted, r: not a bug, t: bug, t: documentation, t: enhancement
- Recent merged examples:
  - #4021 Permit standalone form feed characters at the module level (@tungol)
  - #5080 Fix blackd error handling: split SourceASTParseError from ASTSafetyError (@Bahtya)
  - #4960 Bump docutils, sphinx, myst-parser (@dependabot[bot])
  - #5115 docs: update deprecated PEP URLs to peps.python.org (@cobaltt7)
  - #5111 [pre-commit.ci] pre-commit autoupdate (@pre-commit-ci[bot])
- Recent closed-unmerged examples:
  - #5116 fix: improve diff shades helper edge case handling (@tzgate)
  - #5093 Fix crash when formatting `case case if ...:` with short line lengths (@lawrence3699)
  - #5110 docs: update deprecated PEP URLs to peps.python.org (@Bojun-Vvibe)
  - #5106 docs: fix line-splitting comment wording (@Rohan5commit)

## 5. Textualize/textual

- Activity score: 20.0
- Stars: 35647
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; docs clarifications tied to real behavior or workflow pain; incremental features when they are narrow and clearly justified
- Avoid patterns: generic docs rewrites not tied to a concrete confusion or bug
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; small scoped enhancements after issue-thread alignment
- Signal labels: bug, documentation, enhancement, good first issue, help wanted
- Recent merged examples:
  - #6503 fix anchor release on trackpad (@willmcgugan)
  - #6495 docs: fix input validation typo (@Rohan5commit)
  - #6478 Update classes (@willmcgugan)
  - #6462 [docs] Fix syntax error in app exit code snippet (@IEBqp)
  - #6473 bump (@willmcgugan)
- Recent closed-unmerged examples:
  - #6515 docs: clarify CSS variable scope across stylesheets (@Rohan5commit)
  - #6514 docs: note that thread workers should stay short-lived (@Rohan5commit)
  - #6512 docs: document key identifier format (@Rohan5commit)
  - #6509 fix(work): parameterize Decorator return alias in @work (@Bojun-Vvibe)

## 6. astral-sh/ruff

- Activity score: 20.0
- Stars: 47295
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; incremental features when they are narrow and clearly justified
- Avoid patterns: speculative feature work without prior alignment; generic docs rewrites not tied to a concrete confusion or bug
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; maintainer-tagged onboarding issues
- Signal labels: bug, documentation, good first issue, help wanted
- Recent merged examples:
  - #24924 Simplify the playground's markdown template (@MichaReiser)
  - #24922 Update renovate configuration (@MichaReiser)
  - #24874 Update Renovate configuration (@MichaReiser)
  - #24902 Semantic syntax errors: better error message for global vs parameter (@sharkdp)
  - #24905 [ty] Add missing error context node for protocol to protocol assignability (@sharkdp)
- Recent closed-unmerged examples:
  - #24239 Detect superfluous else on try/except (RET505-508) (@seroperson)
  - #24870 [ty] Make block folding ranges returned by the language server character-precise. (@lerebear)
  - #24442 Fix misleading SIM107 documentation example (@Chessing234)
  - #24908 [ty] Respect client's hover `contentFormat` priority order (@SAY-5)

## 7. microsoft/markitdown

- Activity score: 20.0
- Stars: 118571
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; docs clarifications tied to real behavior or workflow pain; incremental features when they are narrow and clearly justified
- Avoid patterns: speculative feature work without prior alignment
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; small scoped enhancements after issue-thread alignment
- Signal labels: bug, documentation, enhancement, good first issue, help wanted
- Recent merged examples:
  - #1541 [MS] Add OCR layer service for embedded images and PDF scans (@lesyk)
  - #1807 Clarify security posture in READMEs (@afourney)
  - #1644 fix: handle deeply nested HTML that triggers RecursionError (@jigangz)
  - #1551 Remove onnxruntime<=1.20.1 Windows pin (@basnijholt)
  - #1653 Updated warning about binding to non-local interfaces. (@afourney)
- Recent closed-unmerged examples:
  - #1842 Incremental analysis test (@ivanmilevtues)
  - #1840 Add simple web UI for MarkItDown (@NickN0w4k)
  - #1789 fix: redetect plain-text charset after ASCII-only sniff (@lawrence3699)
  - #1739 fix: decode percent-encoded paths in file_uri_to_path (@Jah-yee)

## 8. pallets/click

- Activity score: 20.0
- Stars: 17446
- Good first issue: True
- Help wanted: False
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; maintenance work that aligns with existing tooling and CI conventions; incremental features when they are narrow and clearly justified
- Avoid patterns: broad changes that touch too much for the value delivered
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; maintainer-tagged onboarding issues
- Signal labels: bug, good first issue
- Recent merged examples:
  - #2933 Flush `sys.stderr` when `CliRunner` finalizes (@sirosen)
  - #3363 Auto-detect `type=UNPROCESSED` when `flag_value` has non-basic types (@kdeldycke)
  - #3390 Fix bad merge in changes (@Rowlando13)
  - #3364 Split string values from `default_map` for multi-value parameters (@kdeldycke)
  - #3389 Merge stable into main.  (@Rowlando13)
- Recent closed-unmerged examples:
  - #3392 fix: avoid help option collisions with help arguments (@jaythehardcoder)
  - #3338 Use 'import typing as t' instead of 'import typing' (#3164) (@TanishqGupta1205)
  - #3388 Don't break usage option tokens at internal hyphens (@charlieleith)
  - #3387 Use a private duplicate of stdout/stderr fd in CliRunner (@charlieleith)

## 9. Textualize/rich

- Activity score: 19.0
- Stars: 56224
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; maintenance work that aligns with existing tooling and CI conventions
- Avoid patterns: speculative feature work without prior alignment; generic docs rewrites not tied to a concrete confusion or bug
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; small scoped enhancements after issue-thread alignment
- Signal labels: bug, documentation, enhancement, good first issue, help wanted
- Recent merged examples:
  - #1643 fix detect color (@willmcgugan)
  - #3845 Use faster generator for link IDs (@akx)
  - #4077 proxy isatty (@willmcgugan)
  - #4080 bump to 15.0.0 (@willmcgugan)
  - #4079 Inline table code (@willmcgugan)
- Recent closed-unmerged examples:
  - #4103 Preserve CRLF content in ANSI decoding (@ShipItAndPray)
  - #4101 [DOCKER SEEDING] Add Docker config and run scripts (@BiniamGirmay)
  - #4102 Docker golden solution yml (@BiniamGirmay)
  - #4100 [DOCKER SEEDING] Add Docker config and run scripts (@BiniamGirmay)

## 10. fastapi/fastapi

- Activity score: 19.0
- Stars: 97759
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; incremental features when they are narrow and clearly justified
- Avoid patterns: speculative feature work without prior alignment; drive-by dependency or chore PRs unless explicitly requested
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; small scoped enhancements after issue-thread alignment
- Signal labels: bug, enhancement, good first issue, help wanted
- Recent merged examples:
  - #1 Add tests for path endpoints (@mariacamilagl)
  - #15437 ⬆ Bump sqlmodel from 0.0.32 to 0.0.38 (@dependabot[bot])
  - #15436 ⬆ Bump CodSpeedHQ/action from 4.12.1 to 4.14.0 (@dependabot[bot])
  - #15439 ⬆ Bump pydantic from 2.12.5 to 2.13.2 (@dependabot[bot])
  - #15417 ⬆ Bump pydantic-ai from 1.63.0 to 1.83.0 (@dependabot[bot])
- Recent closed-unmerged examples:
  - #15452 ⬆ Bump click from 8.2.1 to 8.3.2 (@dependabot[bot])
  - #15438 ⬆ Bump pydantic-ai from 1.83.0 to 1.84.1 (@dependabot[bot])
  - #4968 Customizable Request Handler in APIRoute (@sihrc)
  - #13892 md 수정22222 (@fastapi25)

## 11. python-poetry/poetry

- Activity score: 19.0
- Stars: 34279
- Good first issue: True
- Help wanted: False
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; maintenance work that aligns with existing tooling and CI conventions
- Avoid patterns: speculative feature work without prior alignment; generic docs rewrites not tied to a concrete confusion or bug
- Opportunity areas: maintainer-tagged onboarding issues
- Signal labels: good first issue, kind/bug, kind/enhancement
- Recent merged examples:
  - #10790 chore: require new poetry-core version (@radoering)
  - #10791 chore: update json and html fixtures (@radoering)
  - #10792 installer: fix path traversal (@radoering)
  - #10793 release: bump version to 2.3.3 (@radoering)
  - #10795 chore: merge changelog from 2.3.3 and set dev version (@radoering)
- Recent closed-unmerged examples:
  - #10732 fix(publish): normalize legacy repository URL trailing slash (@LouisLau-art)
  - #10859 docs: add documentation build improvements and configuration (@tzgate)
  - #10813 feat: add exclude-newer to filter packages by publish date (@satyamsoni2211)
  - #10763 feat: deferred updates (@marabb01)

## 12. sphinx-doc/sphinx

- Activity score: 19.0
- Stars: 7795
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; docs clarifications tied to real behavior or workflow pain; incremental features when they are narrow and clearly justified
- Avoid patterns: speculative feature work without prior alignment; generic docs rewrites not tied to a concrete confusion or bug
- Opportunity areas: maintainer-tagged onboarding issues
- Signal labels: good first issue, help wanted, type:bug, type:enhancement
- Recent merged examples:
  - #14219 Add app.add_static_dir() API for copying extension static files (@jdillard)
  - #14227 LaTeX: Inhibit breaks for rows with merged vertical cells (@tim-nordell-nimbelink)
  - #14225 Polish CHANGES.rst (@jfbu)
  - #14224 LaTeX: restore 1.7 documentation of literalblockcappos (@jfbu)
  - #14222 LaTeX: improve (again...) some code comments in time for 9.1.0 (@jfbu)
- Recent closed-unmerged examples:
  - #14401 docs: fix intersphinx wording typo (@Rohan5commit)
  - #14358 3.15 support: ensure translated messages are real strings in argparse help and description (@m-aciek)
  - #14398 Update AutoNumbering transform. (@gmilde)
  - #14353 docs: add SECURITY.md with vulnerability reporting policy (@sedat4ras)

## 13. huggingface/datasets

- Activity score: 18.0
- Stars: 21463
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; maintenance work that aligns with existing tooling and CI conventions
- Avoid patterns: speculative feature work without prior alignment; generic docs rewrites not tied to a concrete confusion or bug; drive-by dependency or chore PRs unless explicitly requested
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; small scoped enhancements after issue-thread alignment
- Signal labels: bug, dataset bug, documentation, enhancement, good first issue, help wanted, metric bug
- Recent merged examples:
  - #8158 Dev version (@lhoestq)
  - #8137 Fix: decode JSON type before to_list or to_dict is called (@ItsTania)
  - #8157 Release: 4.8.5 (@lhoestq)
  - #8147 Fix iterable map resume state (@Brianzhengca)
  - #8155 Fix base_path in integration tests (@lhoestq)
- Recent closed-unmerged examples:
  - #8127 Support explicit harness field in agent traces (@jedisct1)
  - #8144 Add Apache TsFile packaged module and Time Series docs category (@Young-Leo)
  - #8138 chore: bump doc-builder SHA for main doc build workflow (@rtrompier)
  - #8111 add sample_by="document" support for jsonl files (@cfahlgren1)

## 14. psf/requests

- Activity score: 18.0
- Stars: 53935
- Good first issue: False
- Help wanted: False
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; docs clarifications tied to real behavior or workflow pain; maintenance work that aligns with existing tooling and CI conventions
- Avoid patterns: broad changes that touch too much for the value delivered
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues
- Signal labels: bug, documentation, question/not a bug
- Recent merged examples:
  - #6939 Bump actions/setup-python from 5.5.0 to 5.6.0 (@dependabot[bot])
  - #7393 Ruff rule UP038 has been removed (@DimitriPapadopoulos)
  - #7390 Bump https://github.com/astral-sh/ruff-pre-commit from v0.15.9 to 0.15.11 in the pre-commit group (@dependabot[bot])
  - #7387 Create groups for GHA and pre-commit dependabot PRs (@nateprewitt)
  - #6937 ci: update to ubuntu-24.04 in workflow (@allrob23)
- Recent closed-unmerged examples:
  - #6940 3.0 (@Abdulkarim28)
  - #7004 Fix-#7003: RequestsCookieJar cannot correctly retrieve zero value (@mengxunQAQ)
  - #7394 PEP 639 compliance (@DimitriPapadopoulos)
  - #7396 Enforce Ruff-specific rules (RUF) (@DimitriPapadopoulos)

## 15. tiangolo/typer

- Activity score: 18.0
- Stars: 19308
- Good first issue: True
- Help wanted: True
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes
- Avoid patterns: broad changes that touch too much for the value delivered
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; maintainer-tagged onboarding issues
- Signal labels: bug, good first issue, help wanted
- Recent merged examples:
  - #1722 ⬆ Bump ruff from 0.15.11 to 0.15.12 (@dependabot[bot])
  - #1723 ⬆ Bump prek from 0.3.10 to 0.3.11 (@dependabot[bot])
  - #1695 🚸 Don't truncate code lines in traceback when formatted with Rich (@YuriiMotov)
  - #1708 🐛 Ensure that `typer.launch` forwards correctly when launching a file (@svlandeg)
  - #1715 ⬆ Bump mypy from 1.20.1 to 1.20.2 (@dependabot[bot])
- Recent closed-unmerged examples:
  - #1208 🐛 Fix `launch` to pass wait and locate parameters to `click.launch` (@phamour)
  - #1717 fix: respect ZDOTDIR when installing zsh completion (@armorbreak001)
  - #1709 Fix typos in internal code comments (@Bojun-Vvibe)
  - #1707 🐛 Fix zsh completion install to respect `$ZDOTDIR` (@barry3406)

## 16. pallets/jinja

- Activity score: 17.0
- Stars: 11597
- Good first issue: True
- Help wanted: False
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: maintenance work that aligns with existing tooling and CI conventions
- Avoid patterns: speculative feature work without prior alignment
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; maintainer-tagged onboarding issues
- Signal labels: bug, good first issue
- Recent merged examples:
  - #2105 remove slsa provenance (@davidism)
  - #2102 svg logo (@davidism)
  - #2093 Updated dependency management to uv (@aenglander)
  - #2096 drop end of life python versions (@davidism)
  - #2097 bump minimum versions of dependencies (@davidism)
- Recent closed-unmerged examples:
  - #2121 Test with python 3.14 (@nsano-rururu)
  - #2154 fix(filters): do not append fill_with when items divide evenly across slices (@justDance-everybody)
  - #2153 Fix slice fill behavior when iterable divides evenly (@BlocksecPHD)
  - #2152 Fix #2118: Slice filter no longer adds extra fill_with items (@MuraveyApp)

## 17. pallets/flask

- Activity score: 16.12
- Stars: 71468
- Good first issue: True
- Help wanted: False
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; maintenance work that aligns with existing tooling and CI conventions; incremental features when they are narrow and clearly justified
- Avoid patterns: speculative feature work without prior alignment; generic docs rewrites not tied to a concrete confusion or bug
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; maintainer-tagged onboarding issues
- Signal labels: bug, good first issue
- Recent merged examples:
  - #5962 remove unicode host test (@davidism)
  - #5945 add zizmor to scan workflows (@davidism)
  - #5928 all teardown callbacks are called despite errors (@davidism)
  - #5924 release version 3.1.3 (@davidism)
  - #5917 fix provide_automatic_options override (@davidism)
- Recent closed-unmerged examples:
  - #5994 <spam> (@samtang-oai)
  - #6010 Add regression tests for session membership access setting Vary: CookieTest patch (@Devansh-66)
  - #6009 Stage (@popeye-007)
  - #5987 fix: upgrade werkzeug to 3.0.3 (CVE-2024-34069) (@orbisai0security)

## 18. pydantic/pydantic

- Activity score: 16.0
- Stars: 27626
- Good first issue: False
- Help wanted: False
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; maintenance work that aligns with existing tooling and CI conventions; incremental features when they are narrow and clearly justified
- Avoid patterns: generic docs rewrites not tied to a concrete confusion or bug
- Opportunity areas: docs clarifications anchored to real issues
- Signal labels: bug v1, bug v2, documentation
- Recent merged examples:
  - #11987 Add regex patterns to JSON schema for `Decimal` type (@Dima-Bulavenko)
  - #11988 Do not emit typechecking error for invalid `Field()` default with `validate_default` set to `True` (@Viicos)
  - #13105 Bump python-dotenv from 1.0.1 to 1.2.2 (@dependabot[bot])
  - #13111 Bump cairosvg from 2.7.1 to 2.9.0 (@dependabot[bot])
  - #13109 Bump libc from 0.2.155 to 0.2.185 (@Viicos)
- Recent closed-unmerged examples:
  - #13126 fix(docs): preserve nested code block indentation (@nightcityblade)
  - #13124 docs: clarify before model validator input (@MestreY0d4-Uninter)
  - #13119 Raise clear TypeError when AliasPath first arg is not a str (@taedaniellim)
  - #13120 docs(validators): document model_validator execution order with inheritance (@MukundaKatta)

## 19. urllib3/urllib3

- Activity score: 16.0
- Stars: 4017
- Good first issue: False
- Help wanted: False
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: small bugfixes and regression-test-backed changes; docs clarifications tied to real behavior or workflow pain; maintenance work that aligns with existing tooling and CI conventions
- Avoid patterns: broad changes that touch too much for the value delivered
- Opportunity areas: small, well-tested fixes matching recent merged PR patterns
- Signal labels: 🐛 confirmed bug
- Recent merged examples:
  - #4973 Upgrade `setup-chrome` and `setup-firefox` to fix warnings (@illia-v)
  - #4967 Prevent content caching after a partial read (@illia-v)
  - #4977 Bump actions/setup-node from 6.3.0 to 6.4.0 (@dependabot[bot])
  - #4976 Bump astral-sh/setup-uv from 8.0.0 to 8.1.0 (@dependabot[bot])
  - #4960 Fix full read with `amt=None` after a partial read (@illia-v)
- Recent closed-unmerged examples:
  - #4975 Fix dynamic default socket options (@ShipItAndPray)
  - #3801 Fix SOCKS proxy auth failure with percent-encoded userinfo (@Krishnachaitanyakc)
  - #4963 CS-2094: Python 3.7 compatibility (@martinPavesio)
  - #3681 Monitor GitHub Actions permissions (@pquentin)

## 20. mkdocs/mkdocs

- Activity score: 15.0
- Stars: 22035
- Good first issue: False
- Help wanted: False
- Why target it: Active maintainers, visible merged external PR flow, and clear labels/scope signals for disciplined contributions.
- Accepted patterns: docs clarifications tied to real behavior or workflow pain; incremental features when they are narrow and clearly justified
- Avoid patterns: speculative feature work without prior alignment; generic docs rewrites not tied to a concrete confusion or bug
- Opportunity areas: bugfixes with regression tests; docs clarifications anchored to real issues; small scoped enhancements after issue-thread alignment
- Signal labels: bug, documentation, enhancement
- Recent merged examples:
  - #3477 Move code to external mkdocs-get-deps dependency (@oprypin)
  - #3631 Release notes for 1.6.0 (@oprypin)
  - #3634 Re-generate localization files (@oprypin)
  - #3493 Update mkdocs theme to bootstrap 5.3 and add support for dark mode. (@waylan)
  - #3629 Drop `changefreq` from `sitemap.xml`. (@lovelydinosaur)
- Recent closed-unmerged examples:
  - #4101 Fix: -v flag suppresses --strict anchor validation (@lawrence3699)
  - #4094 docs: Add details on common mkdocs serve errors (@gemini-25-pro-collab)
  - #4008 Catch exception during initialisation of scrollspy (@ghost)
  - #4007 Fix issue with handling `</>` (@facelessuser)
