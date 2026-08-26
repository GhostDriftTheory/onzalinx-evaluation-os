#!/usr/bin/env python3
"""On the Links Public Claim-to-Evidence Evaluation OS.

A standalone, standard-library-only reference implementation for evaluating the
public alignment between On the Links Co., Ltd.'s declared operational claims
and publicly observable actions and artifacts.

The verification core is intentionally limited to this executable Python file and
one human-readable Markdown report. The HTML summary is a presentation layer, and
JSON certificates are generated only on demand.

Implemented assurance functions:

1. Provenance-bound public source, claim, criterion and evidence universe
2. Investigation-Admissibility Gate over mandatory research obligations,
   uncontrolled-source routes and adverse-candidate dispositions
3. Evidence-mapping completion closure
4. Robust Decision Closure over mapping profiles, criterion weights, thresholds,
   the reference frame and evidence intervals
5. Threshold frontier and conservative manipulation margins
6. Evidence-cluster deletion robustness and criterion leave-one-out analysis
7. Philosophy-to-implementation chain diagnostics
8. Prospective charter freeze payload for later temporal blind commitment
9. Deterministic certificate sealing and full semantic replay

Assurance boundary:
This is a RETROSPECTIVE_TRANSPARENT_PILOT performed by GhostDrift Mathematical
Institute, a disclosed strategic partner and joint AI-assurance implementation
party of the target company. It is not represented as an independent third-party
audit. Evidence intervals are human-authored, source-bound ordinal inputs; the
engine tests which conclusions remain invariant after those inputs are fixed. It
does not determine moral or legal correctness, source truth, or the uniquely
correct interval assignment.

Python: 3.11+
Dependencies: standard library only

Examples:
    python "③評価OS実施コード（オンザリンクス社）.py" evaluate
    python "③評価OS実施コード（オンザリンクス社）.py" self-test
    python "③評価OS実施コード（オンザリンクス社）.py" certificate > certificate.json
    python "③評価OS実施コード（オンザリンクス社）.py" verify certificate.json
    python "③評価OS実施コード（オンザリンクス社）.py" freeze
"""

from __future__ import annotations

import argparse
import ast
import copy
import dataclasses
import enum
import hashlib
import itertools
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, getcontext
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence

getcontext().prec = 50

ENGINE_NAME = "On the Links Claim-to-Evidence Evaluation OS"
ENGINE_VERSION = "1.2.0-final"
CERTIFICATE_SCHEMA = "onzalinx-evaluation-os-certificate/1.2"
ASSESSMENT_MODE = "RETROSPECTIVE_TRANSPARENT_PILOT"
SNAPSHOT_DATE = "2026-08-18"
EVALUATED_AT = "2026-08-18T09:00:00Z"
DEEP_RESEARCH_SHA256 = "77a75672e990c5e2af34ad4264011b537a9c4a20bb76f011e2256b18c19007ae"
STRICT_ESTABLISHMENT_LINE = "68"

STATUS_VALID_RETROSPECTIVE_EVALUATION = "VALID_RETROSPECTIVE_EVALUATION"
STATUS_INVESTIGATION_INCOMPLETE = "INVESTIGATION_INCOMPLETE"
STATUS_MATERIAL_COUNTEREVIDENCE_CONFIRMED = "MATERIAL_COUNTEREVIDENCE_CONFIRMED"
INVESTIGATION_CLOSED = "CLOSED_WITH_UNCONTROLLED_SOURCE_REVIEW"

DIMENSIONS = (
    "claim_specificity",
    "direct_execution",
    "independent_corroboration",
    "temporal_continuity",
    "population_coverage",
    "outcome_verifiability",
)

CORE_CRITERION_IDS = (
    "K_CUSTOMER_OUTCOME",
    "K_USER_AUTONOMY",
    "K_STRUCTURAL_ROI",
    "K_CONTINUOUS_IMPROVEMENT",
    "K_ECOSYSTEM_EXECUTION",
)

EXTENDED_CRITERION_IDS = (
    "K_HIROSHIMA_RESPONSIBLE_AI_EXECUTION",
    "K_INTEGRITY_FAIRNESS_VERIFIABILITY",
)

GLOBAL_INVESTIGATION_REQUIREMENTS = (
    "ENTITY_DUAL_IDENTIFICATION",
    "SOURCE_REGISTER_DISPOSITION",
)

CRITERION_INVESTIGATION_REQUIREMENTS = (
    "OFFICIAL_CLAIM",
    "DIRECT_ACTION_IMPLEMENTATION",
    "TEMPORAL_OR_RECURRING_CONTINUITY",
    "INDEPENDENT_CORROBORATION",
    "LIMITATION_COUNTEREVIDENCE_REVIEW",
    "UNCONTROLLED_ADVERSE_SOURCE_REVIEW",
)

REQUIRED_UNCONTROLLED_ROUTE_IDS = (
    "R_EMPLOYEE_AND_FORMER_EMPLOYEE_REVIEWS",
    "R_PRODUCT_REVIEWS",
    "R_PUBLIC_COMPLAINTS_AND_ATTRIBUTION",
    "R_HIGH_TRUST_ADVERSE_RECORDS",
)

ALLOWED_CANDIDATE_DISPOSITIONS = (
    "ADMITTED_SUPPORT_CONTEXT_ONLY",
    "ADMITTED_TENSION_CONTEXT_ONLY",
    "REJECTED_ENTITY_ATTRIBUTION_UNCONFIRMED",
    "NO_CONFIRMED_MATCH_IN_DECLARED_QUERY_PLAN",
    "ADMITTED_MATERIAL_CORE_REFUTATION",
)

REQUIRED_EVIDENCE_CLUSTERS = ("OFFICIAL_CLAIMS",)
OPTIONAL_CORE_CLUSTERS = (
    "OFFICIAL_PRODUCT_SERVICE",
    "HISTORICAL_CONTINUITY",
    "NAMED_CUSTOMER",
    "PARTNER_PRIMARY",
    "TRADE_AND_INDUSTRY",
    "COMPANY_AGGREGATES",
    "AI_ASSURANCE_CHAIN",
    "CUSTOMER_PURPOSE_COMMITMENT",
    "CUSTOMER_SOVEREIGNTY_ARCHITECTURE",
    "TOC_WHOLE_OPTIMIZATION_CHAIN",
    "CONTINUOUS_GROWTH_MECHANISM",
    "AI_INITIATION_AND_SELECTION",
)

FUTURE_MILESTONES = (
    {
        "milestone_id": "M_HAAC_CONFERENCE_2026_10_14",
        "label": "広島AIアシュアランス協議会カンファレンス",
        "scheduled_date": "2026-10-14",
        "status": "FUTURE_COMMITMENT_NOT_COUNTED_AS_COMPLETED_EVIDENCE",
        "source_basis": "Scheduled public milestone recorded in the fixed research universe; archive the official event page before external production use.",
        "current_score_eligibility": False,
    },
)

EVIDENCE_GROUP_DELETIONS = (
    (
        "DELETE_ALL_AI_ASSURANCE_RELATED",
        ("AI_ASSURANCE_CHAIN", "AI_INITIATION_AND_SELECTION"),
        "Removes both the completed AI-assurance execution chain and the January outreach/selection chain.",
    ),
    (
        "DELETE_INTERSTOCK_CUSTOMER_OPERATING_MODEL",
        ("CUSTOMER_PURPOSE_COMMITMENT", "CUSTOMER_SOVEREIGNTY_ARCHITECTURE", "CONTINUOUS_GROWTH_MECHANISM"),
        "Removes the INTER-STOCK customer-sovereignty, purpose-commitment and continuous-growth mechanisms.",
    ),
    (
        "DELETE_AI_AND_TOC_LONGITUDINAL_CHAINS",
        ("AI_ASSURANCE_CHAIN", "AI_INITIATION_AND_SELECTION", "TOC_WHOLE_OPTIMIZATION_CHAIN"),
        "Removes the AI-assurance chains and the TOC/YUKAI longitudinal chain together.",
    ),
)



# ---------------------------------------------------------------------------
# Deterministic arithmetic and serialization
# ---------------------------------------------------------------------------


def D(value: Any) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        raise TypeError("Boolean values are not valid Decimal inputs")
    if isinstance(value, float):
        # Convert via str to avoid importing the binary representation itself.
        return Decimal(str(value))
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise TypeError(f"Cannot convert {value!r} to Decimal") from exc


def decimal_to_str(value: Decimal) -> str:
    value = D(value)
    if not value.is_finite():
        return str(value)
    if value == 0:
        return "0"
    text = format(value.normalize(), "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def canonicalize(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            field.name: canonicalize(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, enum.Enum):
        return value.value
    if isinstance(value, Decimal):
        return decimal_to_str(value)
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Datetime must be timezone-aware")
        return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")
    if isinstance(value, Mapping):
        return {str(key): canonicalize(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, (tuple, list)):
        return [canonicalize(item) for item in value]
    if isinstance(value, (set, frozenset)):
        normalized = [canonicalize(item) for item in value]
        return sorted(normalized, key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False))
    if isinstance(value, Path):
        return str(value)
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        return decimal_to_str(D(value))
    raise TypeError(f"Unsupported canonical type: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        canonicalize(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_obj(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def is_sha256_hex(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value.lower())


def module_code_hash() -> str:
    try:
        return hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest()
    except (OSError, NameError):
        return sha256_text(f"{ENGINE_NAME}:{ENGINE_VERSION}:source-unavailable")


@dataclass(frozen=True)
class Interval:
    lower: Decimal
    upper: Decimal

    def __post_init__(self) -> None:
        lower = D(self.lower)
        upper = D(self.upper)
        if lower > upper:
            raise ValueError(f"Invalid interval [{lower}, {upper}]")
        object.__setattr__(self, "lower", lower)
        object.__setattr__(self, "upper", upper)

    @staticmethod
    def point(value: Any) -> "Interval":
        value_d = D(value)
        return Interval(value_d, value_d)

    def add(self, other: "Interval") -> "Interval":
        return Interval(self.lower + other.lower, self.upper + other.upper)

    def scale(self, scalar: Any) -> "Interval":
        scalar_d = D(scalar)
        if scalar_d < 0:
            return Interval(scalar_d * self.upper, scalar_d * self.lower)
        return Interval(scalar_d * self.lower, scalar_d * self.upper)

    def clamp(self, lower: Any = 0, upper: Any = 100) -> "Interval":
        lower_d = D(lower)
        upper_d = D(upper)
        return Interval(
            min(upper_d, max(lower_d, self.lower)),
            min(upper_d, max(lower_d, self.upper)),
        )

    def to_obj(self) -> dict[str, str]:
        return {"lower": decimal_to_str(self.lower), "upper": decimal_to_str(self.upper)}


class DecisionStatus(str, enum.Enum):
    ROBUST = "ROBUST"
    INDETERMINATE = "INDETERMINATE"
    INVALID = "INVALID"


# ---------------------------------------------------------------------------
# Public source, claim, evidence, and policy model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceRef:
    source_id: str
    title: str
    locator: str
    publisher: str
    source_class: str
    published_or_observed: str
    content_hash: str
    hash_scope: str
    notes: str = ""


@dataclass(frozen=True)
class ClaimSpec:
    claim_id: str
    criterion_id: str
    label: str
    minimum_public_text: str
    source_ids: tuple[str, ...]
    observability: str
    notes: str = ""


@dataclass(frozen=True)
class CriterionSpec:
    criterion_id: str
    label: str
    claim_id: str
    scope: str
    description: str


@dataclass(frozen=True)
class EvidenceArtifact:
    artifact_id: str
    criterion_id: str
    cluster_id: str
    description: str
    source_ids: tuple[str, ...]
    observed_or_published: str
    feature_intervals: tuple[tuple[str, Interval], ...]
    independence_class: str
    limitations: str

    def feature_map(self) -> dict[str, Interval]:
        return dict(self.feature_intervals)


@dataclass(frozen=True)
class MappingProfile:
    profile_id: str
    label: str
    dimension_weights: tuple[tuple[str, Decimal], ...]
    rationale: str

    def weights(self) -> dict[str, Decimal]:
        return dict(self.dimension_weights)


@dataclass(frozen=True)
class CriterionWeightVertex:
    vertex_id: str
    label: str
    criterion_weights: tuple[tuple[str, Decimal], ...]

    def weights(self) -> dict[str, Decimal]:
        return dict(self.criterion_weights)


@dataclass(frozen=True)
class RatingBand:
    outcome: str
    minimum_score: Decimal


@dataclass(frozen=True)
class ThresholdProfile:
    profile_id: str
    label: str
    group: str
    bands: tuple[RatingBand, ...]


@dataclass(frozen=True)
class ReferenceFrame:
    reference_id: str
    label: str
    method: str
    member_commitment_hash: str


@dataclass(frozen=True)
class FamilyResult:
    mapping_profile_id: str
    weight_vertex_id: str
    threshold_profile_id: str
    reference_frame_id: str
    score_interval: Interval
    outcomes: tuple[str, ...]


@dataclass(frozen=True)
class InvestigationObligationRecord:
    obligation_id: str
    scope_id: str
    requirement_kind: str
    closed: bool
    source_ids: tuple[str, ...]
    notes: str


@dataclass(frozen=True)
class SourceDispositionRecord:
    source_id: str
    status: str
    purposes: tuple[str, ...]


@dataclass(frozen=True)
class UncontrolledSourceRoute:
    route_id: str
    label: str
    completed: bool
    source_ids: tuple[str, ...]
    query_scope: str
    notes: str


@dataclass(frozen=True)
class AdverseCandidateReview:
    candidate_id: str
    source_id: str
    category: str
    reliability: str
    attribution_status: str
    materiality: str
    disposition: str
    unresolved: bool
    material_core_refutation: bool
    notes: str


# ---------------------------------------------------------------------------
# Fixed public source register
# ---------------------------------------------------------------------------


def descriptor_hash(source_id: str, title: str, locator: str, summary: str) -> str:
    return sha256_obj(
        {
            "source_id": source_id,
            "title": title,
            "locator": locator,
            "summary": summary,
            "snapshot_date": SNAPSHOT_DATE,
        }
    )


def source(
    source_id: str,
    title: str,
    locator: str,
    publisher: str,
    source_class: str,
    published_or_observed: str,
    summary: str,
    *,
    actual_hash: Optional[str] = None,
    notes: str = "",
) -> SourceRef:
    return SourceRef(
        source_id=source_id,
        title=title,
        locator=locator,
        publisher=publisher,
        source_class=source_class,
        published_or_observed=published_or_observed,
        content_hash=actual_hash or descriptor_hash(source_id, title, locator, summary),
        hash_scope=(
            "FILE_BYTES"
            if actual_hash is not None
            else "SOURCE_DESCRIPTOR_AND_RESEARCH_EXCERPT_NOT_REMOTE_PAGE_BYTES"
        ),
        notes=notes,
    )


SOURCES = (
    source(
        "S_DEEP_RESEARCH",
        "株式会社オンザリンクス『公開理念―実際の行動』整合性 Deep Research",
        "local://deep-research-report-3.md",
        "Deep Research synthesis",
        "LOCAL_RESEARCH_REPORT",
        SNAPSHOT_DATE,
        "Claim and evidence inventory used as the research basis.",
        actual_hash=DEEP_RESEARCH_SHA256,
    ),
    source(
        "S_VISION",
        "株式会社オンザリンクス 経営理念",
        "https://www.onzalinx.co.jp/vision/index.html",
        "株式会社オンザリンクス",
        "COMPANY_PRIMARY",
        SNAPSHOT_DATE,
        "Customer success and the broad vision 'テクノロジーで世界をもっとやさしく、あたらしく'.",
    ),
    source(
        "S_CREDO",
        "株式会社オンザリンクス 行動指針",
        "https://www.onzalinx.co.jp/vision/credo.html",
        "株式会社オンザリンクス",
        "COMPANY_PRIMARY",
        SNAPSHOT_DATE,
        "Integrity and fairness credo.",
    ),
    source(
        "S_MISSION",
        "株式会社オンザリンクス Our Mission",
        "https://www.onzalinx.co.jp/vision/our_mission.html",
        "株式会社オンザリンクス",
        "COMPANY_PRIMARY",
        SNAPSHOT_DATE,
        "User-led digitalization from inside the enterprise.",
    ),
    source(
        "S_BUSINESS",
        "株式会社オンザリンクス 事業紹介",
        "https://www.onzalinx.co.jp/business/index.html",
        "株式会社オンザリンクス",
        "COMPANY_PRIMARY",
        SNAPSHOT_DATE,
        "Structural diagnosis, ROI, result commitment, post-launch improvement and education.",
    ),
    source(
        "S_PARTNER",
        "株式会社オンザリンクス パートナー",
        "https://www.onzalinx.co.jp/partner/index.html",
        "株式会社オンザリンクス",
        "COMPANY_PRIMARY",
        SNAPSHOT_DATE,
        "OneTeam and partner ecosystem claim.",
    ),
    source(
        "S_INTERSTOCK",
        "INTER-STOCK",
        "https://www.inter-stock.net/",
        "株式会社オンザリンクス",
        "COMPANY_PRODUCT_PRIMARY",
        SNAPSHOT_DATE,
        "Source/DB disclosure, internalization support, named cases, and company aggregate claims.",
    ),
    source(
        "S_INTERNALIZATION_2019",
        "INTER-STOCK内製化支援サービス発表",
        "https://www.value-press.com/pressrelease/229849",
        "株式会社オンザリンクス",
        "DATED_COMPANY_PRIMARY",
        "2019-10-21",
        "Source code and database disclosure with internalization support.",
    ),
    source(
        "S_CODEER",
        "Codeer オンザリンクス導入事例",
        "https://www.codeer.co.jp/LowCode/Ozx",
        "株式会社Codeer",
        "PARTNER_SIDE_PRIMARY",
        "2025",
        "Partner-side confirmation of low-code implementation for On the Links.",
    ),
    source(
        "S_SIGMA",
        "シグマ・インターナショナル会社情報",
        "source-locator-recorded-in-deep-research-report",
        "シグマ・インターナショナル",
        "PARTNER_SIDE_PRIMARY",
        SNAPSHOT_DATE,
        "On the Links listed as a development partner.",
    ),
    source(
        "S_CEC",
        "CEC パートナープログラム 2025年のお知らせ",
        "https://www.cec-ltd.co.jp/partnerprogram/news/2025/",
        "株式会社シーイーシー",
        "PARTNER_SIDE_PRIMARY",
        "2025-10-01",
        "Partner-program membership confirmation.",
    ),
    source(
        "S_TRADE_MEDIA",
        "LNEWS / LOGISTICS TODAY / 日本倉庫協会 関連掲載",
        "multiple://see-deep-research-report",
        "Trade media and industry body",
        "TRADE_OR_INDUSTRY_HOSTED",
        SNAPSHOT_DATE,
        "External hosting of product and case information; many result figures remain company-attributed.",
    ),
    source(
        "S_MARUYOSHI",
        "マルヨシ 内製化事例",
        "source-locator-recorded-in-deep-research-report",
        "株式会社オンザリンクス",
        "NAMED_CUSTOMER_ON_VENDOR_MEDIA",
        "2026-06",
        "Named customer chose source disclosure/internalization support and implemented a function internally.",
    ),
    source(
        "S_YUKAI",
        "YUKAI利益シミュレーションサービス発表",
        "source-locator-recorded-in-deep-research-report",
        "株式会社オンザリンクス",
        "DATED_COMPANY_PRIMARY",
        "2026-07",
        "Simulation of improvement potential from three years of sales, purchase and inventory data.",
    ),
    source(
        "S_INTERSTOCK_POLICY",
        "INTER-STOCK ソース完全公開のこだわり",
        "https://www.inter-stock.net/our-policy/",
        "株式会社オンザリンクス",
        "COMPANY_PRODUCT_PRIMARY",
        SNAPSHOT_DATE,
        "Explicit challenge to vendor lock-in, full source/database disclosure, user-led digitalization, and the credo to attempt what others do not.",
    ),
    source(
        "S_INTERSTOCK_GROWTH",
        "INTER-STOCK 成長型システム",
        "https://www.inter-stock.net/growth/",
        "株式会社オンザリンクス",
        "COMPANY_PRODUCT_PRIMARY",
        SNAPSHOT_DATE,
        "Twice-yearly growth roadmap and version updates plus customer-request upgrade mechanism.",
    ),
    source(
        "S_INTERSTOCK_FEATURE",
        "INTER-STOCK こだわりと強み",
        "https://www.inter-stock.net/feature/",
        "株式会社オンザリンクス",
        "COMPANY_PRODUCT_PRIMARY",
        SNAPSHOT_DATE,
        "Repeated prototypes with customers, no additional cost until stable operation and initial-purpose achievement, and a semi-scratch/open-source operating model.",
    ),
    source(
        "S_YUKAI_2018",
        "オンザリンクス 運送業者レコメンドシステム『輸快通快』β版",
        "https://www.projectdesign.jp/199902/news/004569.php",
        "月刊事業構想 編集部",
        "DATED_TRADE_MEDIA",
        "2018-01-17",
        "Third-party dated report that On the Links announced the YUKAI cloud transport-recommendation service on 2018-01-16.",
    ),
    source(
        "S_TOC_NOTE",
        "売上を減らして利益を2倍にする方法―ボトルネック経営という逆転戦略",
        "https://note.com/higashi_onzalinx/n/na7a3bbef6457",
        "東聖也（株式会社オンザリンクス代表）",
        "PRESIDENT_PRIMARY",
        "2025-10-14",
        "Explicit TOC philosophy: treat the bottleneck as reality and the origin for whole-system optimization; the weakest link determines overall strength.",
    ),
    source(
        "S_YUKAI_2026",
        "輸快通快 正式リリース―AI・数理最適化・TOC",
        "https://prtimes.jp/main/html/rd/p/000000007.000169775.html",
        "株式会社オンザリンクス",
        "DATED_COMPANY_PRIMARY",
        "2026-04-07",
        "YUKAI implementation combines AI demand forecasting, mathematical optimization and TOC, preserves existing systems via API/micro-engines, and frames mathematical optimization as democratization.",
    ),
    source(
        "S_AI_STRATEGY_NOTE",
        "オンザリンクスのAI戦略は、最適化の次へ進む―責任レイヤーという第二段階へ",
        "https://note.com/higashi_onzalinx/n/n0794770663c1",
        "東聖也（株式会社オンザリンクス代表）",
        "PRESIDENT_PRIMARY",
        "2026-05-01",
        "Links the 2018 YUKAI optimization lineage to a responsibility layer requiring evidence, approval and third-party reproducibility.",
    ),
    source(
        "S_GHOSTDRIFT_SELECTION_NOTE",
        "物流AIの判断を証明できるにするために―GhostDrift数理研究所と組んだ3つの理由",
        "https://note.com/higashi_onzalinx/n/nd3c2ff3caa22",
        "東聖也（株式会社オンザリンクス代表）",
        "PRESIDENT_PRIMARY",
        "2026-05-11",
        "Public capability- and values-based partner-selection rationale: aligned ideals, verifiability and complementary field/mathematical capabilities.",
    ),
    source(
        "S_HIROSHIMA_RESPONSIBILITY_NOTE",
        "広島でAIアシュアランスを担う理由―オンザリンクスが引き受ける責任",
        "https://note.com/higashi_onzalinx/n/n5cd55e1ef1b6",
        "東聖也（株式会社オンザリンクス代表）",
        "PRESIDENT_PRIMARY",
        "2026-06-05",
        "Public commitment to be the first social implementer from Hiroshima, preserve conditions/evidence/reproducibility and not ignore people outside optimization.",
    ),
    source(
        "S_AI_OUTREACH_VIDEO",
        "GhostDrift代表インタビュー動画―オンザリンクスによる2026年1月の最初の声掛け証言",
        "https://www.youtube.com/watch?v=KL-y-YmMUrY&t=10s",
        "GhostDrift数理研究所代表（公開動画内証言）",
        "PARTNER_SIDE_PRIMARY_VIDEO_TESTIMONY",
        "2026-08-10",
        "At approximately 00:10 onward, the GhostDrift side states that On the Links first initiated contact in January 2026.",
        notes="User supplied the exact public video and testimony. Production use should archive the video/transcript bytes and timestamped excerpt; this two-file pilot binds the source descriptor only.",
    ),
    source(
        "S_GHOSTDRIFT_COMPANY_OVERVIEW",
        "株式会社GhostDrift数理研究所 会社概要",
        "https://www.ghostdriftresearch.com/company-overview",
        "株式会社GhostDrift数理研究所",
        "PARTNER_COMPANY_PRIMARY",
        SNAPSHOT_DATE,
        "Official company overview states that GhostDrift Mathematical Institute was established on 2026-02-10.",
    ),
    source(
        "S_AI_PARTNERSHIP",
        "オンザリンクス × GhostDrift 戦略的パートナーシップ",
        "https://prtimes.jp/main/html/rd/p/000000008.000169775.html",
        "株式会社オンザリンクス / 株式会社GhostDrift数理研究所",
        "JOINT_PRIMARY",
        "2026-04-28",
        "Partnership signed 2026-04-20 in AI assurance and formal verification-related work.",
    ),
    source(
        "S_AI_PATENT",
        "物流AIの会社判断化に関する共同特許出願",
        "https://prtimes.jp/main/html/rd/p/000000011.000169775.html",
        "株式会社オンザリンクス / 株式会社GhostDrift数理研究所",
        "JOINT_PRIMARY",
        "2026-07-15",
        "Joint patent filing announcement; the release also states planned YUKAI integration, connection to launching the Hiroshima AI Assurance Council, and development toward a common social-implementation protocol.",
    ),
    source(
        "S_AI_POC",
        "医薬品コールドチェーン機械検証PoC第1弾完了・コード公開",
        "https://prtimes.jp/main/html/rd/p/000000005.000182721.html",
        "株式会社オンザリンクス / 株式会社GhostDrift数理研究所",
        "JOINT_PRIMARY",
        "2026-07-28",
        "Completed first PoC and published code, sample data and reproduction instructions; the release identifies it as the first implementation result for the Hiroshima AI Assurance Protocol being developed by the Council in preparation.",
    ),
    source(
        "S_AI_REPOSITORY",
        "coldchain-handoff-assurance repository",
        "https://github.com/GhostDriftTheory/coldchain-handoff-assurance",
        "GhostDriftTheory",
        "PUBLIC_TECHNICAL_ARTIFACT",
        "2026-07-28",
        "Public code and reproducibility artifact for the PoC.",
    ),
    source(
        "S_SECURITY",
        "株式会社オンザリンクス 情報セキュリティ方針・認証表示",
        "source-locator-recorded-in-deep-research-report",
        "株式会社オンザリンクス",
        "COMPANY_PRIMARY",
        SNAPSHOT_DATE,
        "Information-security governance material partially relevant to integrity verifiability.",
    ),
    source(
        "S_COMPANY_OVERVIEW",
        "株式会社オンザリンクス 会社概要",
        "https://www.onzalinx.co.jp/company/index.html",
        "株式会社オンザリンクス",
        "COMPANY_PRIMARY",
        SNAPSHOT_DATE,
        "Official company identity, address and contact information used for entity resolution and complaint-attribution checks.",
    ),
    source(
        "S_GBIZ",
        "Gビズインフォ 株式会社オンザリンクス",
        "https://info.gbiz.go.jp/hojin/ichiran?hojinBango=6240001018929",
        "デジタル庁／Gビズインフォ",
        "PUBLIC_REGISTRY",
        SNAPSHOT_DATE,
        "Public registry record for corporate number 6240001018929, used for dual entity identification and high-trust adverse-record searches.",
    ),
    source(
        "S_EN_JAPAN",
        "エン転職／エン カイシャの評判 株式会社オンザリンクス",
        "https://employment.en-japan.com/comp-130527/",
        "エン・ジャパン株式会社",
        "UNCONTROLLED_EMPLOYEE_REVIEW",
        SNAPSHOT_DATE,
        "Seven-person aggregate is displayed; the detailed public 2024 narrative is one current employee's account, containing both supportive culture observations and competitive/differentiation tensions.",
    ),
    source(
        "S_JOBTALK",
        "転職会議 株式会社オンザリンクスの評判・社風",
        "https://jobtalk.jp/companies/7521921/answers",
        "株式会社リブセンス",
        "UNCONTROLLED_FORMER_EMPLOYEE_REVIEW",
        SNAPSHOT_DATE,
        "One former-employee review, posted in 2017 concerning employment around 2013, describing autonomy, challenge opportunities and shared goals.",
    ),
    source(
        "S_CAREERCONNECTION",
        "キャリコネ 株式会社オンザリンクスのホワイト・ブラック度",
        "https://careerconnection.jp/review/863896/whiteblack/",
        "株式会社グローバルウェイ",
        "UNCONTROLLED_EMPLOYEE_TENSION",
        SNAPSHOT_DATE,
        "One-contributor mixed workplace indicators, including low hours satisfaction, low paid-leave use and reported holiday work; retained as non-material tension context, not a company-wide finding.",
    ),
    source(
        "S_ITREVIEW",
        "ITreview インターストック",
        "https://www.itreview.jp/products/interstock/profile",
        "アイティクラウド株式会社",
        "UNCONTROLLED_PRODUCT_REVIEW",
        SNAPSHOT_DATE,
        "One public product review and displayed satisfaction information; too small a sample for score uplift.",
    ),
    source(
        "S_TELNAVI",
        "電話帳ナビ 050-5482-2314",
        "https://www.telnavi.jp/phone/05054822314",
        "電話帳ナビ",
        "UNCONTROLLED_PUBLIC_COMPLAINT",
        SNAPSHOT_DATE,
        "Six low-rated posts associate the number with On the Links/logistics sales, but the number is absent from the official company contact and some posts describe unrelated asbestos surveys; entity attribution is unconfirmed.",
    ),
    source(
        "S_ADVERSE_SEARCH_RECORD",
        "宣言済み重大不利益情報検索記録",
        "local://onzalinx-adverse-search-plan-2026-08-18",
        "Evaluation OS investigation record",
        "PROCEDURE_BOUNDED_SEARCH_RECORD",
        SNAPSHOT_DATE,
        "Declared searches using the corporate name and number did not identify a confirmed matching administrative sanction, litigation record or major incident within the query plan; this is not proof of nonexistence.",
    ),
)


CLAIMS = (
    ClaimSpec(
        "C001",
        "K_CUSTOMER_OUTCOME",
        "顧客成功・結果コミット",
        "f(success) = 顧客の成功 / 結果にコミット",
        ("S_VISION", "S_BUSINESS"),
        "HIGH_OPERATIONAL_OBSERVABILITY",
    ),
    ClaimSpec(
        "C002",
        "K_USER_AUTONOMY",
        "ユーザー主導・内製化",
        "企業の内側から物流デジタル化を支援",
        ("S_MISSION", "S_INTERSTOCK"),
        "HIGH_OPERATIONAL_OBSERVABILITY",
    ),
    ClaimSpec(
        "C003",
        "K_STRUCTURAL_ROI",
        "物流構造・ROIからの設計",
        "ツールありきではなく、設計ありき",
        ("S_BUSINESS",),
        "HIGH_OPERATIONAL_OBSERVABILITY",
    ),
    ClaimSpec(
        "C004",
        "K_CONTINUOUS_IMPROVEMENT",
        "導入後の継続伴走",
        "導入後も、ずっとパートナー",
        ("S_BUSINESS",),
        "MEDIUM_HIGH_OPERATIONAL_OBSERVABILITY",
    ),
    ClaimSpec(
        "C005",
        "K_ECOSYSTEM_EXECUTION",
        "OneTeam／パートナーエコシステム",
        "OneTeam. One Mission. Unlimited Value.",
        ("S_PARTNER",),
        "HIGH_OPERATIONAL_OBSERVABILITY",
        "The AI-assurance chain is treated as a witness to this source-derived claim, not as a post-hoc standalone criterion.",
    ),
    ClaimSpec(
        "C006",
        "K_HIROSHIMA_RESPONSIBLE_AI_EXECUTION",
        "広島から責任あるAIを社会実装する",
        "社会実装側の第1号として引き受け、判断条件・根拠・証跡・第三者再検証可能性を守る",
        ("S_AI_STRATEGY_NOTE", "S_HIROSHIMA_RESPONSIBILITY_NOTE"),
        "HIGH_CONCRETE_IMPLEMENTATION_OBSERVABILITY",
        "The broad vision 'テクノロジーで世界をもっとやさしく、あたらしく' is context, but this criterion evaluates only the concrete Hiroshima responsible-AI commitment.",
    ),
    ClaimSpec(
        "C007",
        "K_INTEGRITY_FAIRNESS_VERIFIABILITY",
        "誠実・公正",
        "常に誠実・公正に徹する",
        ("S_CREDO",),
        "LOW_ORGANIZATION_WIDE_OBSERVABILITY",
    ),
)


CRITERIA = (
    CriterionSpec(
        "K_CUSTOMER_OUTCOME",
        "Customer outcome accountability",
        "C001",
        "CORE",
        "Public evidence for customer-result commitments, named outcomes and population-level verification.",
    ),
    CriterionSpec(
        "K_USER_AUTONOMY",
        "User autonomy and internalization",
        "C002",
        "CORE",
        "Public evidence for source/DB disclosure, customer-side modification and technology transfer.",
    ),
    CriterionSpec(
        "K_STRUCTURAL_ROI",
        "Structural and ROI discipline",
        "C003",
        "CORE",
        "Public evidence for structural diagnosis, pre-ROI design and post-result verification.",
    ),
    CriterionSpec(
        "K_CONTINUOUS_IMPROVEMENT",
        "Post-launch continuous improvement",
        "C004",
        "CORE",
        "Public evidence for support, KPI review, education and iterative improvement after go-live.",
    ),
    CriterionSpec(
        "K_ECOSYSTEM_EXECUTION",
        "OneTeam and ecosystem execution",
        "C005",
        "CORE",
        "Partner-side confirmation and completed joint implementation artifacts.",
    ),
    CriterionSpec(
        "K_HIROSHIMA_RESPONSIBLE_AI_EXECUTION",
        "Hiroshima responsible-AI execution",
        "C006",
        "EXTENDED",
        "Public evidence that the declared Hiroshima responsible-AI commitment progressed into partnership, joint IP, PoC, reproducibility artifacts, Council preparation and protocol work.",
    ),
    CriterionSpec(
        "K_INTEGRITY_FAIRNESS_VERIFIABILITY",
        "Integrity/fairness public verifiability",
        "C007",
        "EXTENDED",
        "Public observability of organization-wide integrity and fairness execution.",
    ),
)


def fi(**kwargs: tuple[Any, Any]) -> tuple[tuple[str, Interval], ...]:
    unknown = set(kwargs) - set(DIMENSIONS)
    if unknown:
        raise ValueError(f"Unknown dimensions: {sorted(unknown)}")
    return tuple(
        (dimension, Interval(*kwargs[dimension]))
        for dimension in DIMENSIONS
        if dimension in kwargs
    )


ARTIFACTS = (
    # Official claims. These establish what is being evaluated, not whether it was executed.
    EvidenceArtifact("A_C001_CLAIM", "K_CUSTOMER_OUTCOME", "OFFICIAL_CLAIMS", "Repeated explicit customer-success/result commitment.", ("S_VISION", "S_BUSINESS"), SNAPSHOT_DATE, fi(claim_specificity=(4, 4)), "COMPANY_PRIMARY", "Current pages are snapshot-dated; historical wording must not be inferred backward."),
    EvidenceArtifact("A_C002_CLAIM", "K_USER_AUTONOMY", "OFFICIAL_CLAIMS", "Explicit user-led/internalization mission.", ("S_MISSION", "S_INTERSTOCK"), SNAPSHOT_DATE, fi(claim_specificity=(4, 4)), "COMPANY_PRIMARY", "The minimum level of 'self-reliance' remains a charter choice."),
    EvidenceArtifact("A_C003_CLAIM", "K_STRUCTURAL_ROI", "OFFICIAL_CLAIMS", "Explicit structure-first and ROI design claim.", ("S_BUSINESS",), SNAPSHOT_DATE, fi(claim_specificity=(4, 4)), "COMPANY_PRIMARY", "Realized ROI across the total customer population is not implied."),
    EvidenceArtifact("A_C004_CLAIM", "K_CONTINUOUS_IMPROVEMENT", "OFFICIAL_CLAIMS", "Explicit post-launch partnership and improvement claim.", ("S_BUSINESS",), SNAPSHOT_DATE, fi(claim_specificity=(4, 4)), "COMPANY_PRIMARY", "The minimum duration/frequency of continued support remains a charter choice."),
    EvidenceArtifact("A_C005_CLAIM", "K_ECOSYSTEM_EXECUTION", "OFFICIAL_CLAIMS", "Explicit OneTeam/partner-ecosystem claim.", ("S_PARTNER",), SNAPSHOT_DATE, fi(claim_specificity=(4, 4)), "COMPANY_PRIMARY", "Relationship existence and project outcome must be distinguished."),
    EvidenceArtifact("A_C006_CLAIM", "K_HIROSHIMA_RESPONSIBLE_AI_EXECUTION", "OFFICIAL_CLAIMS", "Concrete public commitment to implement verifiable and responsible AI from Hiroshima.", ("S_AI_STRATEGY_NOTE", "S_HIROSHIMA_RESPONSIBILITY_NOTE"), "2026-05-01/2026-06-05", fi(claim_specificity=(4, 4)), "PRESIDENT_PRIMARY", "This criterion does not generalize the result to the company's entire social or environmental vision."),
    EvidenceArtifact("A_C007_CLAIM", "K_INTEGRITY_FAIRNESS_VERIFIABILITY", "OFFICIAL_CLAIMS", "Explicit integrity and fairness credo.", ("S_CREDO",), SNAPSHOT_DATE, fi(claim_specificity=(4, 4)), "COMPANY_PRIMARY", "Absence of adverse reports is not positive evidence."),

    # C001 Customer outcome accountability.
    EvidenceArtifact("A_OUTCOME_SERVICE_MODEL", "K_CUSTOMER_OUTCOME", "OFFICIAL_PRODUCT_SERVICE", "Structural diagnosis, KPI/ROI design, result commitment and continued measurement are presented as the service model.", ("S_BUSINESS",), SNAPSHOT_DATE, fi(direct_execution=(2, 3), independent_corroboration=(1, 1), temporal_continuity=(2, 3), population_coverage=(1, 2), outcome_verifiability=(1, 2)), "COMPANY_PRIMARY", "This verifies service design, not execution for every customer."),
    EvidenceArtifact("A_OUTCOME_NAMED_CASES", "K_CUSTOMER_OUTCOME", "NAMED_CUSTOMER", "Multiple named customer cases and customer statements are publicly presented.", ("S_INTERSTOCK", "S_MARUYOSHI"), "2019-2026", fi(direct_execution=(2, 3), independent_corroboration=(1, 2), temporal_continuity=(2, 3), population_coverage=(2, 2), outcome_verifiability=(2, 3)), "NAMED_CUSTOMER_ON_VENDOR_MEDIA", "Named cases are more specific than anonymous claims but are mostly vendor-hosted."),
    EvidenceArtifact("A_OUTCOME_TRADE_HOSTING", "K_CUSTOMER_OUTCOME", "TRADE_AND_INDUSTRY", "Trade media and an industry body host product/case information.", ("S_TRADE_MEDIA",), SNAPSHOT_DATE, fi(direct_execution=(2, 3), independent_corroboration=(2, 2), temporal_continuity=(2, 2), population_coverage=(1, 2), outcome_verifiability=(1, 2)), "TRADE_OR_INDUSTRY_HOSTED", "Many performance figures remain expressly attributed to the company."),
    EvidenceArtifact("A_OUTCOME_AGGREGATES", "K_CUSTOMER_OUTCOME", "COMPANY_AGGREGATES", "Company pages state 850 installations and very high operation/satisfaction rates.", ("S_INTERSTOCK",), SNAPSHOT_DATE, fi(direct_execution=(1, 2), independent_corroboration=(0, 1), temporal_continuity=(1, 2), population_coverage=(2, 3), outcome_verifiability=(1, 2)), "COMPANY_AGGREGATE_CLAIM", "Denominator, method, period, response rate and independent audit are not publicly reconstructed."),
    EvidenceArtifact("A_OUTCOME_PURPOSE_UNTIL_ACHIEVED", "K_CUSTOMER_OUTCOME", "CUSTOMER_PURPOSE_COMMITMENT", "INTER-STOCK states that engineers develop repeated prototypes with customers and do not charge additional cost until stable operation and the initial purpose are achieved.", ("S_INTERSTOCK_FEATURE",), SNAPSHOT_DATE, fi(direct_execution=(3, 4), independent_corroboration=(1, 1), temporal_continuity=(3, 4), population_coverage=(1, 2), outcome_verifiability=(2, 3)), "COMPANY_PRODUCT_PRIMARY", "This verifies a concrete operating policy, not its population-wide fulfillment rate."),

    # C002 User autonomy/internalization.
    EvidenceArtifact("A_AUTONOMY_2019", "K_USER_AUTONOMY", "HISTORICAL_CONTINUITY", "2019 announcement of source-code/database disclosure and internalization support.", ("S_INTERNALIZATION_2019",), "2019-10-21", fi(direct_execution=(3, 4), independent_corroboration=(1, 1), temporal_continuity=(4, 4), population_coverage=(1, 2), outcome_verifiability=(1, 2)), "DATED_COMPANY_PRIMARY", "The historical customer count is company-reported."),
    EvidenceArtifact("A_AUTONOMY_CURRENT_PRODUCT", "K_USER_AUTONOMY", "OFFICIAL_PRODUCT_SERVICE", "Current product design states source/DB disclosure, user customization and internalization support.", ("S_INTERSTOCK",), SNAPSHOT_DATE, fi(direct_execution=(4, 4), independent_corroboration=(1, 1), temporal_continuity=(3, 4), population_coverage=(1, 2), outcome_verifiability=(1, 2)), "COMPANY_PRODUCT_PRIMARY", "Actual use of the disclosed code by the whole customer population is unknown."),
    EvidenceArtifact("A_AUTONOMY_MARUYOSHI", "K_USER_AUTONOMY", "NAMED_CUSTOMER", "Named customer selected source disclosure/internalization support and implemented a function internally.", ("S_MARUYOSHI",), "2026-06", fi(direct_execution=(3, 4), independent_corroboration=(1, 2), temporal_continuity=(2, 3), population_coverage=(1, 2), outcome_verifiability=(2, 3)), "NAMED_CUSTOMER_ON_VENDOR_MEDIA", "The statement is specific but not customer-hosted."),
    EvidenceArtifact("A_AUTONOMY_CODEER", "K_USER_AUTONOMY", "PARTNER_PRIMARY", "Codeer confirms low-code implementation for On the Links.", ("S_CODEER",), "2025", fi(direct_execution=(3, 4), independent_corroboration=(3, 3), temporal_continuity=(2, 3), population_coverage=(1, 1), outcome_verifiability=(2, 3)), "PARTNER_SIDE_PRIMARY", "Confirms technology implementation, not the proportion of end users achieving full internalization."),
    EvidenceArtifact("A_AUTONOMY_TRADE", "K_USER_AUTONOMY", "TRADE_AND_INDUSTRY", "Trade/industry sources confirm low-code, source disclosure and user customization positioning.", ("S_TRADE_MEDIA",), "2025-2026", fi(direct_execution=(2, 3), independent_corroboration=(2, 2), temporal_continuity=(2, 2), population_coverage=(1, 2), outcome_verifiability=(1, 2)), "TRADE_OR_INDUSTRY_HOSTED", "External hosting is not equivalent to independent performance measurement."),
    EvidenceArtifact("A_AUTONOMY_ANTI_LOCKIN_POLICY", "K_USER_AUTONOMY", "CUSTOMER_SOVEREIGNTY_ARCHITECTURE", "Official policy explicitly challenges vendor lock-in, fully discloses source and database, and shifts the leading role to the user.", ("S_INTERSTOCK_POLICY",), SNAPSHOT_DATE, fi(direct_execution=(4, 4), independent_corroboration=(1, 2), temporal_continuity=(4, 4), population_coverage=(2, 2), outcome_verifiability=(2, 3)), "COMPANY_PRODUCT_PRIMARY", "The architecture and policy are directly observable; population-wide customer autonomy remains unmeasured."),

    # C003 Structural/ROI discipline.
    EvidenceArtifact("A_ROI_SERVICE_MODEL", "K_STRUCTURAL_ROI", "OFFICIAL_PRODUCT_SERVICE", "Current business model specifies structural diagnosis, ROI presentation, KPI design and measurement.", ("S_BUSINESS",), SNAPSHOT_DATE, fi(direct_execution=(3, 4), independent_corroboration=(1, 1), temporal_continuity=(2, 3), population_coverage=(1, 2), outcome_verifiability=(1, 2)), "COMPANY_PRIMARY", "Verifies the model exists; not the realized ROI distribution."),
    EvidenceArtifact("A_ROI_YUKAI", "K_STRUCTURAL_ROI", "OFFICIAL_PRODUCT_SERVICE", "YUKAI simulates improvement potential from three years of transaction/inventory data.", ("S_YUKAI",), "2026-07", fi(direct_execution=(3, 4), independent_corroboration=(1, 1), temporal_continuity=(2, 3), population_coverage=(1, 1), outcome_verifiability=(1, 2)), "DATED_COMPANY_PRIMARY", "Pre-decision simulation is not evidence that projected ROI was realized."),
    EvidenceArtifact("A_ROI_NAMED_CASES", "K_STRUCTURAL_ROI", "NAMED_CUSTOMER", "Named cases include specific operational improvements and selection reasons.", ("S_INTERSTOCK", "S_MARUYOSHI"), "2019-2026", fi(direct_execution=(2, 3), independent_corroboration=(1, 2), temporal_continuity=(2, 3), population_coverage=(1, 2), outcome_verifiability=(2, 3)), "NAMED_CUSTOMER_ON_VENDOR_MEDIA", "Methods, baselines and causal attribution are not consistently public."),
    EvidenceArtifact("A_ROI_TRADE", "K_STRUCTURAL_ROI", "TRADE_AND_INDUSTRY", "Trade media report product and case developments.", ("S_TRADE_MEDIA",), "2025-2026", fi(direct_execution=(2, 3), independent_corroboration=(2, 2), temporal_continuity=(2, 2), population_coverage=(1, 2), outcome_verifiability=(1, 2)), "TRADE_OR_INDUSTRY_HOSTED", "Performance figures are often company-attributed."),
    EvidenceArtifact("A_ROI_TOC_YUKAI_CHAIN", "K_STRUCTURAL_ROI", "TOC_WHOLE_OPTIMIZATION_CHAIN", "Public chain from the 2018 YUKAI transport-recommendation service, through the president's explicit TOC bottleneck philosophy, to the 2026 YUKAI implementation combining AI, mathematical optimization and TOC.", ("S_YUKAI_2018", "S_TOC_NOTE", "S_YUKAI_2026"), "2018-01-16/2026-04-07", fi(direct_execution=(4, 4), independent_corroboration=(2, 2), temporal_continuity=(4, 4), population_coverage=(2, 2), outcome_verifiability=(2, 3)), "DATED_COMPANY_PRIMARY_PLUS_TRADE_PRIMARY", "Shows philosophy-to-product implementation and longitudinal continuity; published ROI figures are not independently audited."),

    # C004 Continuous improvement.
    EvidenceArtifact("A_CONTINUITY_SERVICE_MODEL", "K_CONTINUOUS_IMPROVEMENT", "OFFICIAL_PRODUCT_SERVICE", "Post-launch support, KPI review, education and improvement cycles are explicitly offered.", ("S_BUSINESS",), SNAPSHOT_DATE, fi(direct_execution=(2, 3), independent_corroboration=(1, 1), temporal_continuity=(2, 3), population_coverage=(1, 2), outcome_verifiability=(1, 2)), "COMPANY_PRIMARY", "Customer-level duration, frequency, SLA and continuation rate are not public."),
    EvidenceArtifact("A_CONTINUITY_CASES", "K_CONTINUOUS_IMPROVEMENT", "NAMED_CUSTOMER", "Named cases indicate continued operational support and evolution after introduction.", ("S_INTERSTOCK",), "2019-2026", fi(direct_execution=(2, 3), independent_corroboration=(1, 2), temporal_continuity=(2, 3), population_coverage=(1, 2), outcome_verifiability=(1, 2)), "NAMED_CUSTOMER_ON_VENDOR_MEDIA", "The full support history for each customer is not available."),
    EvidenceArtifact("A_CONTINUITY_TRADE", "K_CONTINUOUS_IMPROVEMENT", "TRADE_AND_INDUSTRY", "External sources confirm continued product evolution and support positioning.", ("S_TRADE_MEDIA",), "2025-2026", fi(direct_execution=(1, 2), independent_corroboration=(2, 2), temporal_continuity=(2, 2), population_coverage=(1, 1), outcome_verifiability=(1, 1)), "TRADE_OR_INDUSTRY_HOSTED", "Product evolution is not identical to a verified customer-level improvement cycle."),
    EvidenceArtifact("A_CONTINUITY_GROWTH_MECHANISM", "K_CONTINUOUS_IMPROVEMENT", "CONTINUOUS_GROWTH_MECHANISM", "INTER-STOCK publishes a twice-yearly growth roadmap, twice-yearly version updates, a customer-request upgrade scheme, and repeated prototypes until stable operation and initial-purpose achievement.", ("S_INTERSTOCK_GROWTH", "S_INTERSTOCK_FEATURE"), SNAPSHOT_DATE, fi(direct_execution=(4, 4), independent_corroboration=(1, 1), temporal_continuity=(4, 4), population_coverage=(2, 3), outcome_verifiability=(2, 3)), "COMPANY_PRODUCT_PRIMARY", "The mechanism is explicit; actual execution frequency and customer-level outcomes are not independently reconstructed."),

    # C005 Ecosystem/OneTeam. AI assurance is a witness to this existing claim.
    EvidenceArtifact("A_ECOSYSTEM_OFFICIAL", "K_ECOSYSTEM_EXECUTION", "OFFICIAL_PRODUCT_SERVICE", "Official partner structure and OneTeam operating model are public.", ("S_PARTNER",), SNAPSHOT_DATE, fi(direct_execution=(2, 3), independent_corroboration=(1, 1), temporal_continuity=(2, 3), population_coverage=(2, 3), outcome_verifiability=(1, 2)), "COMPANY_PRIMARY", "An official partner list proves the declared model and relationships claimed by the company, not every project's outcome."),
    EvidenceArtifact("A_ECOSYSTEM_CODEER", "K_ECOSYSTEM_EXECUTION", "PARTNER_PRIMARY", "Codeer confirms a concrete technology implementation for On the Links.", ("S_CODEER",), "2025", fi(direct_execution=(3, 4), independent_corroboration=(3, 3), temporal_continuity=(2, 3), population_coverage=(1, 2), outcome_verifiability=(2, 3)), "PARTNER_SIDE_PRIMARY", "One partner implementation cannot represent the complete ecosystem."),
    EvidenceArtifact("A_ECOSYSTEM_SIGMA_CEC", "K_ECOSYSTEM_EXECUTION", "PARTNER_PRIMARY", "Sigma and CEC independently confirm partner relationships.", ("S_SIGMA", "S_CEC"), "2025-2026", fi(direct_execution=(2, 3), independent_corroboration=(3, 3), temporal_continuity=(2, 3), population_coverage=(2, 2), outcome_verifiability=(1, 2)), "PARTNER_SIDE_PRIMARY", "Relationship existence is stronger than evidence of quantified joint outcomes."),
    EvidenceArtifact("A_ECOSYSTEM_AI_ASSURANCE_CHAIN", "K_ECOSYSTEM_EXECUTION", "AI_ASSURANCE_CHAIN", "Partnership, joint patent, completed PoC and public reproducibility artifact in a novel AI-assurance domain.", ("S_AI_PARTNERSHIP", "S_AI_PATENT", "S_AI_POC", "S_AI_REPOSITORY"), "2026-04-20/2026-07-28", fi(direct_execution=(4, 4), independent_corroboration=(3, 3), temporal_continuity=(3, 3), population_coverage=(1, 1), outcome_verifiability=(3, 4)), "JOINT_PRIMARY_PLUS_PUBLIC_TECHNICAL_ARTIFACT", "A completed single chain is strong evidence of execution but not commercial-scale adoption or universal innovation capability."),
    EvidenceArtifact("A_ECOSYSTEM_INITIATION_SELECTION", "K_ECOSYSTEM_EXECUTION", "AI_INITIATION_AND_SELECTION", "Partner-side public video testimony states that On the Links initiated contact in January 2026; the president later published a capability- and values-based partner-selection rationale, followed by patent, PoC and public code.", ("S_AI_OUTREACH_VIDEO", "S_GHOSTDRIFT_COMPANY_OVERVIEW", "S_GHOSTDRIFT_SELECTION_NOTE", "S_AI_PATENT", "S_AI_POC", "S_AI_REPOSITORY"), "2026-01/2026-07-28", fi(direct_execution=(4, 4), independent_corroboration=(3, 3), temporal_continuity=(4, 4), population_coverage=(2, 2), outcome_verifiability=(3, 4)), "PARTNER_SIDE_PRIMARY_PLUS_JOINT_ARTIFACTS", "One high-quality chain does not establish universal partner-selection quality."),

    # Extended concrete public-value execution and integrity verifiability.
    EvidenceArtifact("A_HIROSHIMA_RESPONSIBLE_AI_CHAIN", "K_HIROSHIMA_RESPONSIBLE_AI_EXECUTION", "HIROSHIMA_RESPONSIBILITY_CHAIN", "The president publicly committed On the Links to implement AI assurance from Hiroshima and not ignore people outside optimization; the parties then advanced through joint patent, Council preparation, completed PoC, public code and protocol work.", ("S_AI_STRATEGY_NOTE", "S_GHOSTDRIFT_SELECTION_NOTE", "S_HIROSHIMA_RESPONSIBILITY_NOTE", "S_AI_PATENT", "S_AI_POC", "S_AI_REPOSITORY"), "2026-05-01/2026-07-28", fi(direct_execution=(4, 4), independent_corroboration=(2, 3), temporal_continuity=(4, 4), population_coverage=(1, 1), outcome_verifiability=(3, 4)), "COMPANY_AND_PARTNER_PRIMARY_PLUS_PUBLIC_TECHNICAL_ARTIFACT", "Strong for one concrete responsible-AI implementation chain; it does not measure the full environmental or society-wide impact of the broad vision."),
    EvidenceArtifact("A_INTEGRITY_SECURITY", "K_INTEGRITY_FAIRNESS_VERIFIABILITY", "CSR_AND_GOVERNANCE", "Information-security governance materials provide partial objective structure.", ("S_SECURITY",), SNAPSHOT_DATE, fi(direct_execution=(1, 2), independent_corroboration=(1, 2), temporal_continuity=(1, 2), population_coverage=(0, 1), outcome_verifiability=(0, 1)), "COMPANY_PRIMARY_WITH_CERTIFICATION_REFERENCE", "Security governance does not establish organization-wide integrity, grievance handling or contractual fairness."),
)


MAPPING_PROFILES = (
    MappingProfile(
        "M_BALANCED",
        "Balanced evidence interpretation",
        tuple((key, D(value)) for key, value in (
            ("claim_specificity", "0.15"),
            ("direct_execution", "0.25"),
            ("independent_corroboration", "0.20"),
            ("temporal_continuity", "0.15"),
            ("population_coverage", "0.10"),
            ("outcome_verifiability", "0.15"),
        )),
        "Balances explicit claim, execution, independence, time, breadth and outcome evidence.",
    ),
    MappingProfile(
        "M_ACTION_HEAVY",
        "Action/artifact-heavy interpretation",
        tuple((key, D(value)) for key, value in (
            ("claim_specificity", "0.10"),
            ("direct_execution", "0.35"),
            ("independent_corroboration", "0.15"),
            ("temporal_continuity", "0.15"),
            ("population_coverage", "0.10"),
            ("outcome_verifiability", "0.15"),
        )),
        "Gives more weight to completed artifacts while retaining all dimensions.",
    ),
    MappingProfile(
        "M_INDEPENDENCE_HEAVY",
        "Independent-corroboration-heavy interpretation",
        tuple((key, D(value)) for key, value in (
            ("claim_specificity", "0.10"),
            ("direct_execution", "0.20"),
            ("independent_corroboration", "0.30"),
            ("temporal_continuity", "0.10"),
            ("population_coverage", "0.15"),
            ("outcome_verifiability", "0.15"),
        )),
        "Stress-tests company-controlled evidence by emphasizing independent corroboration.",
    ),
    MappingProfile(
        "M_POPULATION_SKEPTICAL",
        "Population/outcome skeptical interpretation",
        tuple((key, D(value)) for key, value in (
            ("claim_specificity", "0.10"),
            ("direct_execution", "0.20"),
            ("independent_corroboration", "0.20"),
            ("temporal_continuity", "0.10"),
            ("population_coverage", "0.20"),
            ("outcome_verifiability", "0.20"),
        )),
        "Penalizes evidence universes that lack denominators, failures and independently measured outcomes.",
    ),
)


BASE_CORE_WEIGHTS = (
    CriterionWeightVertex(
        "W_BALANCED",
        "Balanced",
        tuple((cid, D("0.20")) for cid in CORE_CRITERION_IDS),
    ),
    CriterionWeightVertex(
        "W_CUSTOMER_VALUE",
        "Customer outcome and ROI emphasis",
        tuple((cid, D(value)) for cid, value in zip(CORE_CRITERION_IDS, ("0.30", "0.15", "0.25", "0.15", "0.15"))),
    ),
    CriterionWeightVertex(
        "W_AUTONOMY",
        "User autonomy emphasis",
        tuple((cid, D(value)) for cid, value in zip(CORE_CRITERION_IDS, ("0.15", "0.30", "0.20", "0.15", "0.20"))),
    ),
    CriterionWeightVertex(
        "W_CONTINUITY",
        "Continuous improvement emphasis",
        tuple((cid, D(value)) for cid, value in zip(CORE_CRITERION_IDS, ("0.20", "0.15", "0.20", "0.30", "0.15"))),
    ),
    CriterionWeightVertex(
        "W_ECOSYSTEM",
        "Ecosystem execution emphasis",
        tuple((cid, D(value)) for cid, value in zip(CORE_CRITERION_IDS, ("0.15", "0.15", "0.15", "0.20", "0.35"))),
    ),
)

EXTENDED_WEIGHTS = (
    CriterionWeightVertex("W_EXT_BALANCED", "Balanced extended evaluation", ((EXTENDED_CRITERION_IDS[0], D("0.50")), (EXTENDED_CRITERION_IDS[1], D("0.50")))),
    CriterionWeightVertex("W_EXT_SOCIAL", "Hiroshima responsible-AI emphasis", ((EXTENDED_CRITERION_IDS[0], D("0.60")), (EXTENDED_CRITERION_IDS[1], D("0.40")))),
    CriterionWeightVertex("W_EXT_INTEGRITY", "Integrity/fairness emphasis", ((EXTENDED_CRITERION_IDS[0], D("0.40")), (EXTENDED_CRITERION_IDS[1], D("0.60")))),
)


THRESHOLDS = (
    ThresholdProfile(
        "T_CORE_BASELINE",
        "Core alignment baseline",
        "CORE_COARSE",
        (
            RatingBand("PUBLIC_ALIGNMENT_ESTABLISHED", D("55")),
            RatingBand("PARTIAL_PUBLIC_ALIGNMENT", D("40")),
            RatingBand("PUBLIC_EVIDENCE_INSUFFICIENT", D("0")),
        ),
    ),
    ThresholdProfile(
        "T_CORE_STANDARD",
        "Core alignment standard",
        "CORE_COARSE",
        (
            RatingBand("PUBLIC_ALIGNMENT_ESTABLISHED", D("60")),
            RatingBand("PARTIAL_PUBLIC_ALIGNMENT", D("45")),
            RatingBand("PUBLIC_EVIDENCE_INSUFFICIENT", D("0")),
        ),
    ),
    ThresholdProfile(
        "T_CORE_STRICT",
        "Core alignment strict",
        "CORE_COARSE",
        (
            RatingBand("PUBLIC_ALIGNMENT_ESTABLISHED", D(STRICT_ESTABLISHMENT_LINE)),
            RatingBand("PARTIAL_PUBLIC_ALIGNMENT", D("50")),
            RatingBand("PUBLIC_EVIDENCE_INSUFFICIENT", D("0")),
        ),
    ),
    ThresholdProfile(
        "T_FINE_STANDARD",
        "Fine strength standard",
        "CORE_FINE",
        (
            RatingBand("VERY_STRONG_PUBLIC_ALIGNMENT", D("85")),
            RatingBand("STRONG_PUBLIC_ALIGNMENT", D("70")),
            RatingBand("MODERATE_PUBLIC_ALIGNMENT", D("55")),
            RatingBand("LIMITED_PUBLIC_ALIGNMENT", D("0")),
        ),
    ),
    ThresholdProfile(
        "T_FINE_STRICT",
        "Fine strength strict",
        "CORE_FINE",
        (
            RatingBand("VERY_STRONG_PUBLIC_ALIGNMENT", D("90")),
            RatingBand("STRONG_PUBLIC_ALIGNMENT", D("75")),
            RatingBand("MODERATE_PUBLIC_ALIGNMENT", D("60")),
            RatingBand("LIMITED_PUBLIC_ALIGNMENT", D("0")),
        ),
    ),
    ThresholdProfile(
        "T_EXTENDED_STANDARD",
        "Extended public-verifiability standard",
        "EXTENDED",
        (
            RatingBand("PUBLIC_VALUE_EXECUTION_ESTABLISHED", D("65")),
            RatingBand("PARTIALLY_EVIDENCED", D("40")),
            RatingBand("PUBLICLY_INDETERMINATE", D("0")),
        ),
    ),
    ThresholdProfile(
        "T_EXTENDED_STRICT",
        "Extended public-verifiability strict",
        "EXTENDED",
        (
            RatingBand("PUBLIC_VALUE_EXECUTION_ESTABLISHED", D("70")),
            RatingBand("PARTIALLY_EVIDENCED", D("45")),
            RatingBand("PUBLICLY_INDETERMINATE", D("0")),
        ),
    ),
)

REFERENCE_FRAMES = (
    ReferenceFrame(
        "R_SELF_DECLARED_ABSOLUTE",
        "Self-declared claim frame",
        "ABSOLUTE_CLAIM_TO_EVIDENCE_NO_PEER_COMPARISON",
        sha256_text("On the Links self-declared public claim frame"),
    ),
)


def evaluation_metadata() -> dict[str, Any]:
    return canonicalize(
        {
            "assessment_mode": ASSESSMENT_MODE,
            "snapshot_date": SNAPSHOT_DATE,
            "evaluated_at": EVALUATED_AT,
            "target_entity_id": "JP-6240001018929",
            "target_entity_name": "株式会社オンザリンクス",
            "evaluator_entity_name": "株式会社GhostDrift数理研究所",
            "evaluator_role": "EVALUATION_SYSTEM_DESIGNER_AND_PUBLIC_EVIDENCE_ASSESSOR",
            "evaluator_relationship_to_target": "STRATEGIC_PARTNER_AND_JOINT_AI_ASSURANCE_IMPLEMENTATION_PARTY",
            "evaluation_character": "RELATIONSHIP_DISCLOSED_REPRODUCIBLE_PUBLIC_EVIDENCE_ASSESSMENT",
            "independent_third_party_audit_claimed": False,
            "evidence_interval_assignment_mode": "HUMAN_AUTHORED_SOURCE_BOUND_ORDINAL_INTERVAL",
            "temporal_blind_commitment_claim": False,
            "external_timestamp_verified": False,
            "research_basis_sha256": DEEP_RESEARCH_SHA256,
            "score_semantics": "PUBLIC_CLAIM_TO_EVIDENCE_ALIGNMENT_STRENGTH_NOT_COMPANY_PERFORMANCE_PERCENTAGE",
            "source_universe_policy": "PUBLIC_SOURCES_AND_EVIDENCE_ARTIFACTS_FIXED_AT_THE_DECLARED_SNAPSHOT_DATE",
        }
    )


def source_hash_policy() -> dict[str, str]:
    return {
        "remote_pages": "Descriptor-and-research-excerpt hashes are used because archived remote page bytes were not bundled in this public package.",
        "research_report": "The Deep Research Markdown byte hash is fixed.",
        "production_requirement": "Archive page bytes/PDFs and bind them to external trusted timestamps and signatures.",
    }


def evidence_level_scale() -> dict[str, Any]:
    return canonicalize(
        {
            "minimum": 0,
            "maximum": 4,
            "assignment_policy": {
                "mode": "HUMAN_AUTHORED_SOURCE_BOUND_ORDINAL_INTERVAL",
                "machine_derived": False,
                "unique_correctness_claimed": False,
                "bounds": "INTEGER_0_TO_4",
                "bound_semantics": "The lower bound is the least defensible public-support level and the upper bound is the greatest defensible level under the declared anchors.",
                "required_context": ["source_ids", "description", "independence_class", "limitations"],
                "challenge_rule": "A disputed interval must be changed inside the fixed evaluation universe, which changes the universe hash and certificate and requires complete replay.",
            },
            "generic_meaning": {
                "0": "No guaranteed public support for this dimension; not proof of real-world failure.",
                "1": "Declaration, service design or isolated/self-controlled evidence.",
                "2": "Specific named or externally hosted evidence, but limited independence or coverage.",
                "3": "Strong repeated, partner-side, multi-date or outcome-specific evidence.",
                "4": "Exceptional direct execution, continuity or independently verified population-level evidence, depending on dimension.",
            },
            "dimension_anchors": {
                "claim_specificity": {
                    "0": "No identifiable public claim.",
                    "1": "Broad aspiration without an operational object or condition.",
                    "2": "Specific subject but limited operational or testable content.",
                    "3": "Operational claim with an identifiable object, action or expected condition.",
                    "4": "Explicit, source-bound and testable commitment with identifiable conditions or outcomes.",
                },
                "direct_execution": {
                    "0": "No guaranteed public execution evidence.",
                    "1": "Declared policy, service design or intended operating model.",
                    "2": "Specific activity or isolated implementation evidence.",
                    "3": "Completed named implementation or directly inspectable artifact.",
                    "4": "Directly inspectable completed implementation chain or reproducible technical artifact.",
                },
                "independent_corroboration": {
                    "0": "No corroboration beyond the evaluator's assertion.",
                    "1": "Target-controlled or same-side source only.",
                    "2": "External hosting, named-party evidence or limited uncontrolled-source support.",
                    "3": "Partner/customer-side primary evidence or independent dated confirmation.",
                    "4": "Independent audit, reproduction or population-level confirmation.",
                },
                "temporal_continuity": {
                    "0": "No dated continuity is guaranteed.",
                    "1": "One current or isolated temporal observation.",
                    "2": "Multiple dates or a recurring mechanism with limited duration evidence.",
                    "3": "Repeated multi-year execution or an explicit recurring operating mechanism.",
                    "4": "Long-running multi-period chain with direct continuity across major milestones.",
                },
                "population_coverage": {
                    "0": "No observable coverage is guaranteed.",
                    "1": "One isolated case or narrow instance.",
                    "2": "Multiple named cases or partial-segment coverage.",
                    "3": "Broad repeated cases or a meaningful aggregate with stated denominator or method.",
                    "4": "Independently verified population-wide coverage.",
                },
                "outcome_verifiability": {
                    "0": "No observable outcome is guaranteed.",
                    "1": "Intended outcome or service design only.",
                    "2": "Specific result with incomplete method, baseline or attribution.",
                    "3": "Outcome-specific evidence with reproducible artifact or partner-side confirmation.",
                    "4": "Independently measured, audited or reproduced outcome at the relevant scale.",
                },
            },
            "mapping_to_score": "Each ordinal level is mapped linearly to 25 score points before profile weighting.",
        }
    )


def evaluation_restrictions() -> dict[str, Any]:
    return canonicalize(
        {
            "core_criterion_universe": list(CORE_CRITERION_IDS),
            "extended_criterion_universe": list(EXTENDED_CRITERION_IDS),
            "post_hoc_novel_domain_criterion_prohibited": True,
            "ai_assurance_treatment": "Evidence witness for C005/K_ECOSYSTEM_EXECUTION plus separate categorical diagnostic.",
            "unknown_not_real_world_failure": True,
            "evidence_interval_machine_derived": False,
            "evidence_interval_unique_correctness_claimed": False,
            "evidence_interval_source_binding_required": True,
            "evidence_interval_limitations_required": True,
            "relationship_disclosure_required": True,
            "independent_third_party_audit_claimed": False,
            "peer_comparison_excluded": True,
            "mapping_profiles_all_admissible": True,
            "all_core_weight_vertices_admissible": True,
            "all_declared_threshold_profiles_admissible": True,
            "reference_frame": "R_SELF_DECLARED_ABSOLUTE",
        }
    )


def trusted_evaluation_universe_payload() -> dict[str, Any]:
    """Engine-side fixed numerical/research universe for this named evaluation."""
    return canonicalize(
        {
            "metadata": evaluation_metadata(),
            "source_hash_policy": source_hash_policy(),
            "evidence_level_scale": evidence_level_scale(),
            "sources": SOURCES,
            "claims": CLAIMS,
            "criteria": CRITERIA,
            "artifacts": ARTIFACTS,
            "mapping_profiles": MAPPING_PROFILES,
            "weight_vertices": BASE_CORE_WEIGHTS + EXTENDED_WEIGHTS,
            "threshold_profiles": THRESHOLDS,
            "reference_frames": REFERENCE_FRAMES,
            "future_milestones_not_scored": FUTURE_MILESTONES,
            "restrictions": evaluation_restrictions(),
        }
    )


def trusted_evaluation_universe_hash() -> str:
    return sha256_obj(trusted_evaluation_universe_payload())


def manifest_evaluation_universe_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return canonicalize(
        {
            key: manifest[key]
            for key in (
                "metadata",
                "source_hash_policy",
                "evidence_level_scale",
                "sources",
                "claims",
                "criteria",
                "artifacts",
                "mapping_profiles",
                "weight_vertices",
                "threshold_profiles",
                "reference_frames",
                "future_milestones_not_scored",
                "restrictions",
            )
        }
    )


# ---------------------------------------------------------------------------
# Validation and reconstruction
# ---------------------------------------------------------------------------


def source_map(sources: Sequence[SourceRef]) -> dict[str, SourceRef]:
    return {item.source_id: item for item in sources}


def criterion_map(criteria: Sequence[CriterionSpec]) -> dict[str, CriterionSpec]:
    return {item.criterion_id: item for item in criteria}


def validate_manifest(manifest: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    required_top_level = {
        "metadata",
        "source_hash_policy",
        "evidence_level_scale",
        "sources",
        "claims",
        "criteria",
        "artifacts",
        "mapping_profiles",
        "weight_vertices",
        "threshold_profiles",
        "reference_frames",
        "future_milestones_not_scored",
        "restrictions",
        "investigation_assurance",
    }
    missing = required_top_level - set(manifest)
    extra = set(manifest) - required_top_level
    if missing:
        errors.append(f"manifest missing required fields: {sorted(missing)}")
    if extra:
        errors.append(f"manifest contains undeclared fields: {sorted(extra)}")
    if errors:
        return errors
    if manifest["metadata"].get("snapshot_date") != SNAPSHOT_DATE:
        errors.append("manifest snapshot_date differs from engine snapshot")
    if manifest["metadata"].get("evaluated_at") != EVALUATED_AT:
        errors.append("manifest evaluated_at differs from engine evaluation time")
    if manifest["metadata"].get("target_entity_id") != "JP-6240001018929":
        errors.append("manifest target_entity_id differs from the fixed evaluation target")
    if manifest["metadata"].get("target_entity_name") != "株式会社オンザリンクス":
        errors.append("manifest target_entity_name differs from the fixed evaluation target")
    if manifest["metadata"].get("evaluator_entity_name") != "株式会社GhostDrift数理研究所":
        errors.append("manifest evaluator identity differs from the disclosed evaluator")
    if manifest["metadata"].get("evaluator_relationship_to_target") != "STRATEGIC_PARTNER_AND_JOINT_AI_ASSURANCE_IMPLEMENTATION_PARTY":
        errors.append("manifest evaluator relationship disclosure differs from the fixed disclosure")
    if manifest["metadata"].get("independent_third_party_audit_claimed") is not False:
        errors.append("manifest must not represent this evaluation as an independent third-party audit")
    if manifest["metadata"].get("evidence_interval_assignment_mode") != "HUMAN_AUTHORED_SOURCE_BOUND_ORDINAL_INTERVAL":
        errors.append("manifest evidence interval assignment mode differs from the fixed disclosure")
    assignment_policy = manifest.get("evidence_level_scale", {}).get("assignment_policy", {})
    if assignment_policy.get("machine_derived") is not False:
        errors.append("evidence intervals must be disclosed as human-authored inputs")
    if assignment_policy.get("unique_correctness_claimed") is not False:
        errors.append("evidence interval unique correctness must not be claimed")
    if assignment_policy.get("bounds") != "INTEGER_0_TO_4":
        errors.append("evidence interval bounds policy differs from the fixed ordinal policy")
    if sha256_obj(manifest_evaluation_universe_payload(manifest)) != trusted_evaluation_universe_hash():
        errors.append("retrospective evaluation universe differs from the engine-side fixed universe")

    sources = parse_sources(manifest["sources"])
    claims = parse_claims(manifest["claims"])
    criteria = parse_criteria(manifest["criteria"])
    artifacts = parse_artifacts(manifest["artifacts"])
    mappings = parse_mapping_profiles(manifest["mapping_profiles"])
    weights = parse_weight_vertices(manifest["weight_vertices"])
    thresholds = parse_threshold_profiles(manifest["threshold_profiles"])
    references = parse_reference_frames(manifest["reference_frames"])

    def duplicates(values: Iterable[str]) -> set[str]:
        seen: set[str] = set()
        out: set[str] = set()
        for value in values:
            if value in seen:
                out.add(value)
            seen.add(value)
        return out

    for label, values in (
        ("source", [item.source_id for item in sources]),
        ("claim", [item.claim_id for item in claims]),
        ("criterion", [item.criterion_id for item in criteria]),
        ("artifact", [item.artifact_id for item in artifacts]),
        ("mapping", [item.profile_id for item in mappings]),
        ("weight", [item.vertex_id for item in weights]),
        ("threshold", [item.profile_id for item in thresholds]),
        ("reference", [item.reference_id for item in references]),
    ):
        for duplicate in duplicates(values):
            errors.append(f"duplicate {label} identifier: {duplicate}")

    source_ids = {item.source_id for item in sources}
    criterion_ids = {item.criterion_id for item in criteria}
    claim_ids = {item.claim_id for item in claims}
    for item in sources:
        if not is_sha256_hex(item.content_hash):
            errors.append(f"invalid source hash: {item.source_id}")
    for item in claims:
        if item.criterion_id not in criterion_ids:
            errors.append(f"claim {item.claim_id} references unknown criterion")
        for sid in item.source_ids:
            if sid not in source_ids:
                errors.append(f"claim {item.claim_id} references unknown source {sid}")
    for item in criteria:
        if item.claim_id not in claim_ids:
            errors.append(f"criterion {item.criterion_id} references unknown claim")
    for item in artifacts:
        if item.criterion_id not in criterion_ids:
            errors.append(f"artifact {item.artifact_id} references unknown criterion")
        if not item.source_ids:
            errors.append(f"artifact {item.artifact_id} has no source binding")
        if not item.description.strip():
            errors.append(f"artifact {item.artifact_id} has no public description")
        if not item.independence_class.strip():
            errors.append(f"artifact {item.artifact_id} has no independence classification")
        if not item.limitations.strip():
            errors.append(f"artifact {item.artifact_id} has no stated limitations")
        if not item.feature_intervals:
            errors.append(f"artifact {item.artifact_id} has no evidence interval")
        for sid in item.source_ids:
            if sid not in source_ids:
                errors.append(f"artifact {item.artifact_id} references unknown source {sid}")
        dimensions = [key for key, _ in item.feature_intervals]
        if len(dimensions) != len(set(dimensions)):
            errors.append(f"artifact {item.artifact_id} repeats a dimension")
        for dimension, interval in item.feature_intervals:
            if dimension not in DIMENSIONS:
                errors.append(f"artifact {item.artifact_id} uses unknown dimension {dimension}")
            if interval.lower < 0 or interval.upper > 4:
                errors.append(f"artifact {item.artifact_id} level outside [0,4]")
            if interval.lower != interval.lower.to_integral_value() or interval.upper != interval.upper.to_integral_value():
                errors.append(f"artifact {item.artifact_id} interval bounds must be integer ordinal levels")
    for profile in mappings:
        values = profile.weights()
        if set(values) != set(DIMENSIONS):
            errors.append(f"mapping profile {profile.profile_id} dimension mismatch")
        if any(value < 0 for value in values.values()):
            errors.append(f"mapping profile {profile.profile_id} contains negative weight")
        if sum(values.values(), D(0)) != D(1):
            errors.append(f"mapping profile {profile.profile_id} weights do not sum to 1")
    for vertex in weights:
        values = vertex.weights()
        if any(value < 0 for value in values.values()):
            errors.append(f"weight vertex {vertex.vertex_id} contains negative weight")
        if sum(values.values(), D(0)) != D(1):
            errors.append(f"weight vertex {vertex.vertex_id} weights do not sum to 1")
        if not set(values).issubset(criterion_ids):
            errors.append(f"weight vertex {vertex.vertex_id} references unknown criterion")
    for profile in thresholds:
        if not profile.bands:
            errors.append(f"threshold profile {profile.profile_id} has no bands")
            continue
        minima = [band.minimum_score for band in profile.bands]
        if any(minima[index] <= minima[index + 1] for index in range(len(minima) - 1)):
            errors.append(f"threshold profile {profile.profile_id} bands are not strictly descending")
        if minima[-1] != D(0):
            errors.append(f"threshold profile {profile.profile_id} does not cover score zero")
    if not references:
        errors.append("no reference frame")
    for frame in references:
        if not is_sha256_hex(frame.member_commitment_hash):
            errors.append(f"reference frame {frame.reference_id} has invalid commitment hash")

    if "K_NOVEL_DOMAIN_EXECUTION" in criterion_ids:
        errors.append("post-hoc standalone novel-domain criterion is prohibited by the declared charter")

    core_thresholds = [profile for profile in thresholds if profile.group == "CORE_COARSE"]
    core_pass_lines = sorted(
        band.minimum_score
        for profile in core_thresholds
        for band in profile.bands
        if band.outcome == "PUBLIC_ALIGNMENT_ESTABLISHED"
    )
    if core_pass_lines != [D("55"), D("60"), D(STRICT_ESTABLISHMENT_LINE)]:
        errors.append("CORE_COARSE establishment lines must be exactly 55, 60 and 68")
    if len(sources) != 38:
        errors.append(f"fixed source register must contain 38 sources, found {len(sources)}")
    return errors


def parse_interval(obj: Mapping[str, Any]) -> Interval:
    return Interval(obj["lower"], obj["upper"])


def parse_sources(values: Sequence[Mapping[str, Any]]) -> tuple[SourceRef, ...]:
    return tuple(SourceRef(**dict(item)) for item in values)


def parse_claims(values: Sequence[Mapping[str, Any]]) -> tuple[ClaimSpec, ...]:
    return tuple(
        ClaimSpec(
            claim_id=item["claim_id"],
            criterion_id=item["criterion_id"],
            label=item["label"],
            minimum_public_text=item["minimum_public_text"],
            source_ids=tuple(item["source_ids"]),
            observability=item["observability"],
            notes=item.get("notes", ""),
        )
        for item in values
    )


def parse_criteria(values: Sequence[Mapping[str, Any]]) -> tuple[CriterionSpec, ...]:
    return tuple(CriterionSpec(**dict(item)) for item in values)


def parse_artifacts(values: Sequence[Mapping[str, Any]]) -> tuple[EvidenceArtifact, ...]:
    return tuple(
        EvidenceArtifact(
            artifact_id=item["artifact_id"],
            criterion_id=item["criterion_id"],
            cluster_id=item["cluster_id"],
            description=item["description"],
            source_ids=tuple(item["source_ids"]),
            observed_or_published=item["observed_or_published"],
            feature_intervals=tuple(
                (dimension, parse_interval(interval_obj))
                for dimension, interval_obj in item["feature_intervals"]
            ),
            independence_class=item["independence_class"],
            limitations=item["limitations"],
        )
        for item in values
    )


def parse_mapping_profiles(values: Sequence[Mapping[str, Any]]) -> tuple[MappingProfile, ...]:
    return tuple(
        MappingProfile(
            profile_id=item["profile_id"],
            label=item["label"],
            dimension_weights=tuple((key, D(value)) for key, value in item["dimension_weights"]),
            rationale=item["rationale"],
        )
        for item in values
    )


def parse_weight_vertices(values: Sequence[Mapping[str, Any]]) -> tuple[CriterionWeightVertex, ...]:
    return tuple(
        CriterionWeightVertex(
            vertex_id=item["vertex_id"],
            label=item["label"],
            criterion_weights=tuple((key, D(value)) for key, value in item["criterion_weights"]),
        )
        for item in values
    )


def parse_threshold_profiles(values: Sequence[Mapping[str, Any]]) -> tuple[ThresholdProfile, ...]:
    return tuple(
        ThresholdProfile(
            profile_id=item["profile_id"],
            label=item["label"],
            group=item["group"],
            bands=tuple(RatingBand(band["outcome"], D(band["minimum_score"])) for band in item["bands"]),
        )
        for item in values
    )


def parse_reference_frames(values: Sequence[Mapping[str, Any]]) -> tuple[ReferenceFrame, ...]:
    return tuple(ReferenceFrame(**dict(item)) for item in values)


# ---------------------------------------------------------------------------
# Evaluation mathematics
# ---------------------------------------------------------------------------


def aggregate_feature_intervals(
    criterion_id: str,
    artifacts: Sequence[EvidenceArtifact],
    *,
    excluded_clusters: frozenset[str] = frozenset(),
    included_optional_clusters: Optional[frozenset[str]] = None,
) -> dict[str, Interval]:
    selected: list[EvidenceArtifact] = []
    for artifact in artifacts:
        if artifact.criterion_id != criterion_id:
            continue
        if artifact.cluster_id in excluded_clusters:
            continue
        if included_optional_clusters is not None:
            if artifact.cluster_id not in REQUIRED_EVIDENCE_CLUSTERS and artifact.cluster_id not in included_optional_clusters:
                continue
        selected.append(artifact)

    out: dict[str, Interval] = {}
    for dimension in DIMENSIONS:
        intervals = [artifact.feature_map()[dimension] for artifact in selected if dimension in artifact.feature_map()]
        if intervals:
            out[dimension] = Interval(
                max(item.lower for item in intervals),
                max(item.upper for item in intervals),
            )
        else:
            # Zero is a lower bound on guaranteed public support for this dimension,
            # not a claim that the underlying real-world behavior failed.
            out[dimension] = Interval(0, 0)
    return out


def map_features_to_score(features: Mapping[str, Interval], profile: MappingProfile) -> Interval:
    score = Interval.point(0)
    for dimension, weight in profile.weights().items():
        # Ordinal evidence level 0..4 is mapped linearly to 0..100.
        score = score.add(features[dimension].scale(weight * D(25)))
    return score.clamp(0, 100)


def criterion_score_intervals(
    criterion_ids: Sequence[str],
    artifacts: Sequence[EvidenceArtifact],
    mapping_profile: MappingProfile,
    *,
    excluded_clusters: frozenset[str] = frozenset(),
    included_optional_clusters: Optional[frozenset[str]] = None,
) -> dict[str, Interval]:
    return {
        criterion_id: map_features_to_score(
            aggregate_feature_intervals(
                criterion_id,
                artifacts,
                excluded_clusters=excluded_clusters,
                included_optional_clusters=included_optional_clusters,
            ),
            mapping_profile,
        )
        for criterion_id in criterion_ids
    }


def weighted_score_interval(
    criterion_scores: Mapping[str, Interval],
    vertex: CriterionWeightVertex,
) -> Interval:
    score = Interval.point(0)
    for criterion_id, weight in vertex.weights().items():
        score = score.add(criterion_scores[criterion_id].scale(weight))
    return score.clamp(0, 100)


def possible_outcomes(profile: ThresholdProfile, score_interval: Interval) -> tuple[str, ...]:
    outcomes: set[str] = set()
    bands = profile.bands
    for index, band in enumerate(bands):
        lower = band.minimum_score
        upper = None if index == 0 else bands[index - 1].minimum_score
        lower_reachable = score_interval.upper >= lower
        upper_reachable = upper is None or score_interval.lower < upper
        if lower_reachable and upper_reachable:
            outcomes.add(band.outcome)
    return tuple(sorted(outcomes))


def restrict_and_renormalize_vertices(
    vertices: Sequence[CriterionWeightVertex], criterion_ids: Sequence[str]
) -> tuple[CriterionWeightVertex, ...]:
    criterion_set = set(criterion_ids)
    out: list[CriterionWeightVertex] = []
    seen: set[tuple[tuple[str, str], ...]] = set()
    for vertex in vertices:
        restricted = {cid: weight for cid, weight in vertex.weights().items() if cid in criterion_set}
        total = sum(restricted.values(), D(0))
        if total <= 0:
            continue
        normalized = {cid: weight / total for cid, weight in restricted.items()}
        signature = tuple(sorted((cid, decimal_to_str(weight)) for cid, weight in normalized.items()))
        if signature in seen:
            continue
        seen.add(signature)
        out.append(
            CriterionWeightVertex(
                f"{vertex.vertex_id}__RESTRICTED",
                f"{vertex.label} (renormalized)",
                tuple((cid, normalized[cid]) for cid in criterion_ids),
            )
        )
    return tuple(out)


def evaluate_universe(
    *,
    criterion_ids: Sequence[str],
    artifacts: Sequence[EvidenceArtifact],
    mapping_profiles: Sequence[MappingProfile],
    weight_vertices: Sequence[CriterionWeightVertex],
    threshold_profiles: Sequence[ThresholdProfile],
    reference_frames: Sequence[ReferenceFrame],
    excluded_clusters: frozenset[str] = frozenset(),
    included_optional_clusters: Optional[frozenset[str]] = None,
) -> dict[str, Any]:
    if not criterion_ids or not mapping_profiles or not weight_vertices or not threshold_profiles or not reference_frames:
        return {
            "status": DecisionStatus.INVALID.value,
            "possible_outcomes": [],
            "robust_outcome": None,
            "selector_immunity": False,
            "family_count": 0,
            "score_envelope": None,
            "threshold_frontier": None,
            "families": [],
            "manipulation_geometry": None,
        }

    families: list[FamilyResult] = []
    all_outcomes: set[str] = set()
    all_scores: list[Interval] = []
    for mapping_profile, vertex, threshold_profile, reference in itertools.product(
        mapping_profiles, weight_vertices, threshold_profiles, reference_frames
    ):
        scores = criterion_score_intervals(
            criterion_ids,
            artifacts,
            mapping_profile,
            excluded_clusters=excluded_clusters,
            included_optional_clusters=included_optional_clusters,
        )
        interval = weighted_score_interval(scores, vertex)
        outcomes = possible_outcomes(threshold_profile, interval)
        families.append(
            FamilyResult(
                mapping_profile.profile_id,
                vertex.vertex_id,
                threshold_profile.profile_id,
                reference.reference_id,
                interval,
                outcomes,
            )
        )
        all_outcomes.update(outcomes)
        all_scores.append(interval)

    status = DecisionStatus.ROBUST if len(all_outcomes) == 1 else DecisionStatus.INDETERMINATE
    robust_outcome = next(iter(all_outcomes)) if status == DecisionStatus.ROBUST else None
    lower_frontier = min(interval.lower for interval in all_scores)
    upper_frontier = max(interval.upper for interval in all_scores)

    margin: Optional[Decimal] = None
    if robust_outcome is not None:
        margins: list[Decimal] = []
        threshold_by_id = {profile.profile_id: profile for profile in threshold_profiles}
        for family in families:
            profile = threshold_by_id[family.threshold_profile_id]
            for index, band in enumerate(profile.bands):
                if band.outcome != robust_outcome:
                    continue
                lower_margin = family.score_interval.lower - band.minimum_score
                upper = None if index == 0 else profile.bands[index - 1].minimum_score
                margins.append(lower_margin if upper is None else min(lower_margin, upper - family.score_interval.upper))
        if margins:
            margin = min(margins)

    witnesses: dict[str, dict[str, Any]] = {}
    for family in families:
        for outcome in family.outcomes:
            witnesses.setdefault(
                outcome,
                {
                    "mapping_profile_id": family.mapping_profile_id,
                    "weight_vertex_id": family.weight_vertex_id,
                    "threshold_profile_id": family.threshold_profile_id,
                    "reference_frame_id": family.reference_frame_id,
                    "score_interval": family.score_interval.to_obj(),
                },
            )

    return {
        "status": status.value,
        "possible_outcomes": sorted(all_outcomes),
        "robust_outcome": robust_outcome,
        "selector_immunity": status == DecisionStatus.ROBUST,
        "family_count": len(families),
        "score_envelope": Interval(lower_frontier, upper_frontier).to_obj(),
        "threshold_frontier": {
            "guaranteed_lower_score": decimal_to_str(lower_frontier),
            "possible_upper_score": decimal_to_str(upper_frontier),
            "interpretation": (
                "For every admissible mapping profile, criterion-weight vertex, reference frame and evidence completion, "
                f"the aggregate score is at least {decimal_to_str(lower_frontier)}. Any pass threshold at or below that lower frontier is robust."
            ),
        },
        "witnesses": witnesses,
        "manipulation_geometry": (
            None
            if margin is None
            else {
                "score_boundary_margin": decimal_to_str(margin),
                "uniform_threshold_shift_strictly_less_than": decimal_to_str(margin),
                "additional_score_linf_strictly_less_than": decimal_to_str(margin),
                "additional_weight_l1_strictly_less_than": decimal_to_str(margin / D(100)),
                "scope": "Conservative inner bounds inside the declared profile universe; profile additions are tested separately, not covered by this scalar margin.",
            }
        ),
        "families": [canonicalize(family) for family in families],
    }


def core_threshold_profiles(thresholds: Sequence[ThresholdProfile], group: str) -> tuple[ThresholdProfile, ...]:
    return tuple(item for item in thresholds if item.group == group)


def criterion_diagnostics(
    criterion_ids: Sequence[str],
    artifacts: Sequence[EvidenceArtifact],
    mapping_profiles: Sequence[MappingProfile],
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for criterion_id in criterion_ids:
        profile_results: dict[str, Any] = {}
        lower_values: list[Decimal] = []
        upper_values: list[Decimal] = []
        features = aggregate_feature_intervals(criterion_id, artifacts)
        for profile in mapping_profiles:
            interval = map_features_to_score(features, profile)
            profile_results[profile.profile_id] = interval.to_obj()
            lower_values.append(interval.lower)
            upper_values.append(interval.upper)
        out[criterion_id] = {
            "feature_intervals": {dimension: features[dimension].to_obj() for dimension in DIMENSIONS},
            "mapping_profile_scores": profile_results,
            "mapping_envelope": Interval(min(lower_values), max(upper_values)).to_obj(),
        }
    return out


def evidence_deletion_analysis(
    manifest_objects: Mapping[str, Any],
    *,
    target_thresholds: Sequence[Decimal] = (D("55"), D("60"), D(STRICT_ESTABLISHMENT_LINE)),
) -> dict[str, Any]:
    criteria = tuple(item.criterion_id for item in manifest_objects["criteria"] if item.scope == "CORE")
    artifacts = manifest_objects["artifacts"]
    mappings = manifest_objects["mapping_profiles"]
    vertices = tuple(item for item in manifest_objects["weight_vertices"] if set(item.weights()) == set(CORE_CRITERION_IDS))
    references = manifest_objects["reference_frames"]
    # A threshold profile is not needed to calculate the invariant lower frontier;
    # use one dummy profile to reuse the family evaluator.
    frontier_profile = (
        ThresholdProfile("T_FRONTIER", "Threshold frontier", "FRONTIER", (RatingBand("ABOVE_ZERO", D(0)),)),
    )

    scenarios: dict[str, Any] = {}
    for cluster in OPTIONAL_CORE_CLUSTERS:
        result = evaluate_universe(
            criterion_ids=criteria,
            artifacts=artifacts,
            mapping_profiles=mappings,
            weight_vertices=vertices,
            threshold_profiles=frontier_profile,
            reference_frames=references,
            excluded_clusters=frozenset({cluster}),
        )
        lower = D(result["threshold_frontier"]["guaranteed_lower_score"])
        scenarios[f"DELETE_{cluster}"] = {
            "excluded_cluster": cluster,
            "score_envelope": result["score_envelope"],
            "guaranteed_lower_score": decimal_to_str(lower),
            "robust_thresholds": {
                decimal_to_str(threshold): lower >= threshold for threshold in target_thresholds
            },
        }
    return scenarios


def evidence_group_deletion_analysis(
    manifest_objects: Mapping[str, Any],
    *,
    target_thresholds: Sequence[Decimal] = (D("55"), D("60"), D(STRICT_ESTABLISHMENT_LINE), D("70")),
) -> dict[str, Any]:
    criteria = tuple(item.criterion_id for item in manifest_objects["criteria"] if item.scope == "CORE")
    artifacts = manifest_objects["artifacts"]
    mappings = manifest_objects["mapping_profiles"]
    vertices = tuple(item for item in manifest_objects["weight_vertices"] if set(item.weights()) == set(CORE_CRITERION_IDS))
    references = manifest_objects["reference_frames"]
    frontier_profile = (
        ThresholdProfile("T_FRONTIER_GROUP_DELETE", "Threshold frontier", "FRONTIER", (RatingBand("ABOVE_ZERO", D(0)),)),
    )
    scenarios: dict[str, Any] = {}
    for scenario_id, clusters, description in EVIDENCE_GROUP_DELETIONS:
        result = evaluate_universe(
            criterion_ids=criteria,
            artifacts=artifacts,
            mapping_profiles=mappings,
            weight_vertices=vertices,
            threshold_profiles=frontier_profile,
            reference_frames=references,
            excluded_clusters=frozenset(clusters),
        )
        lower = D(result["threshold_frontier"]["guaranteed_lower_score"])
        scenarios[scenario_id] = {
            "excluded_clusters": list(clusters),
            "description": description,
            "score_envelope": result["score_envelope"],
            "guaranteed_lower_score": decimal_to_str(lower),
            "robust_thresholds": {
                decimal_to_str(threshold): lower >= threshold for threshold in target_thresholds
            },
        }
    return scenarios


def criterion_leave_one_out_analysis(manifest_objects: Mapping[str, Any]) -> dict[str, Any]:
    criteria = tuple(item.criterion_id for item in manifest_objects["criteria"] if item.scope == "CORE")
    artifacts = manifest_objects["artifacts"]
    mappings = manifest_objects["mapping_profiles"]
    base_vertices = tuple(item for item in manifest_objects["weight_vertices"] if set(item.weights()) == set(CORE_CRITERION_IDS))
    references = manifest_objects["reference_frames"]
    coarse = tuple(item for item in manifest_objects["threshold_profiles"] if item.group == "CORE_COARSE")
    out: dict[str, Any] = {}
    for removed in criteria:
        remaining = tuple(item for item in criteria if item != removed)
        vertices = restrict_and_renormalize_vertices(base_vertices, remaining)
        result = evaluate_universe(
            criterion_ids=remaining,
            artifacts=artifacts,
            mapping_profiles=mappings,
            weight_vertices=vertices,
            threshold_profiles=coarse,
            reference_frames=references,
        )
        out[f"REMOVE_{removed}"] = {
            "removed_criterion": removed,
            "remaining_criteria": list(remaining),
            "status": result["status"],
            "possible_outcomes": result["possible_outcomes"],
            "score_envelope": result["score_envelope"],
            "threshold_frontier": result["threshold_frontier"],
        }
    return out


def philosophy_to_implementation_chains(sources: Sequence[SourceRef]) -> dict[str, Any]:
    active = {item.source_id for item in sources}

    def chain(chain_id: str, label: str, milestones: Sequence[tuple[str, str]], inference: str, limitations: Sequence[str]) -> dict[str, Any]:
        status = {name: source_id in active for name, source_id in milestones}
        return {
            "chain_id": chain_id,
            "label": label,
            "milestones": status,
            "completed_milestones": sum(status.values()),
            "required_milestones": len(status),
            "chain_outcome": "COMPLETE_PUBLIC_CLAIM_TO_IMPLEMENTATION_CHAIN" if all(status.values()) else "INCOMPLETE_CHAIN",
            "supported_inference": inference,
            "limitations": list(limitations),
        }

    return {
        "customer_sovereignty": chain(
            "CHAIN_CUSTOMER_SOVEREIGNTY",
            "顧客へシステム主導権を戻す",
            (
                ("explicit_anti_lockin_and_user_led_policy", "S_INTERSTOCK_POLICY"),
                ("2019_source_and_database_disclosure", "S_INTERNALIZATION_2019"),
                ("partner_confirmed_lowcode_implementation", "S_CODEER"),
                ("named_customer_internal_implementation", "S_MARUYOSHI"),
            ),
            "The public record connects an anti-lock-in/user-led policy to product architecture, partner implementation and a named customer-side modification case.",
            ("Population-wide internalization rates and contract details remain unpublished.",),
        ),
        "constraint_centered_whole_optimization": chain(
            "CHAIN_TOC_WHOLE_OPTIMIZATION",
            "最弱環・制約を起点に全体を強くする",
            (
                ("2018_yukai_transport_recommendation", "S_YUKAI_2018"),
                ("explicit_toc_bottleneck_philosophy", "S_TOC_NOTE"),
                ("2026_yukai_ai_math_toc_implementation", "S_YUKAI_2026"),
            ),
            "The public record connects a long-running optimization product lineage with an explicit TOC philosophy and a current TOC-embedded implementation.",
            ("TOC concerns system constraints/weakest links; it should not be paraphrased as a literal claim about socially weak persons without additional evidence.", "Published ROI figures remain company-reported."),
        ),
        "hiroshima_responsible_ai": chain(
            "CHAIN_HIROSHIMA_RESPONSIBLE_AI",
            "広島から責任あるAIを制度・実装へ移す",
            (
                ("partner_side_testimony_of_january_outreach", "S_AI_OUTREACH_VIDEO"),
                ("strategic_partnership", "S_AI_PARTNERSHIP"),
                ("responsibility_layer_strategy_note", "S_AI_STRATEGY_NOTE"),
                ("public_partner_selection_rationale", "S_GHOSTDRIFT_SELECTION_NOTE"),
                ("hiroshima_responsibility_commitment", "S_HIROSHIMA_RESPONSIBILITY_NOTE"),
                ("joint_patent_and_council_progression", "S_AI_PATENT"),
                ("completed_poc_public_code_and_protocol_work", "S_AI_POC"),
            ),
            "The public record supports a proactive, capability-based co-creation chain that moved from outreach and public rationale to patent, PoC, open reproducibility artifacts, Council preparation and protocol work.",
            ("The October 2026 conference is a future milestone and is not counted as completed evidence.", "Commercial-scale adoption and world leadership are not established."),
        ),
    }


def individual_extended_frontiers(manifest_objects: Mapping[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    thresholds = core_threshold_profiles(manifest_objects["threshold_profiles"], "EXTENDED")
    for criterion_id in EXTENDED_CRITERION_IDS:
        result = evaluate_universe(
            criterion_ids=(criterion_id,),
            artifacts=manifest_objects["artifacts"],
            mapping_profiles=manifest_objects["mapping_profiles"],
            weight_vertices=(CriterionWeightVertex(f"W_ONLY_{criterion_id}", "Single criterion", ((criterion_id, D(1)),)),),
            threshold_profiles=thresholds,
            reference_frames=manifest_objects["reference_frames"],
        )
        out[criterion_id] = {
            "status": result["status"],
            "possible_outcomes": result["possible_outcomes"],
            "score_envelope": result["score_envelope"],
            "threshold_frontier": result["threshold_frontier"],
        }
    return out


def ai_assurance_witness(artifacts: Sequence[EvidenceArtifact]) -> dict[str, Any]:
    milestone_sources = {
        "initial_outreach_by_onzalinx": "S_AI_OUTREACH_VIDEO",
        "strategic_partnership": "S_AI_PARTNERSHIP",
        "public_partner_selection_rationale": "S_GHOSTDRIFT_SELECTION_NOTE",
        "joint_patent": "S_AI_PATENT",
        "completed_poc": "S_AI_POC",
        "public_reproducibility_artifact": "S_AI_REPOSITORY",
    }
    active_source_ids = {
        source_id
        for artifact in artifacts
        if artifact.cluster_id in {"AI_ASSURANCE_CHAIN", "AI_INITIATION_AND_SELECTION"}
        for source_id in artifact.source_ids
    }
    completion = {key: source_id in active_source_ids for key, source_id in milestone_sources.items()}
    count = sum(completion.values())
    return {
        "diagnostic_type": "SOURCE_DERIVED_C005_WITNESS_NOT_STANDALONE_CRITERION",
        "milestones": completion,
        "completed_milestones": count,
        "required_milestones": len(milestone_sources),
        "witness_outcome": "COMPLETED_PROACTIVE_NOVEL_DOMAIN_CO_CREATION_CHAIN" if count == len(milestone_sources) else "INCOMPLETE_CHAIN",
        "timeline": {
            "initial_outreach_testified": "2026-01",
            "ghostdrift_corporation_established": "2026-02-10",
            "partnership_signed": "2026-04-20",
            "partnership_announced": "2026-04-28",
            "partner_selection_note": "2026-05-11",
            "joint_patent_announced": "2026-07-15",
            "poc_completed_and_code_published": "2026-07-28",
        },
        "supported_inference": "A partner-side public testimony says On the Links initiated contact in January 2026, before the GhostDrift corporation was established; the public record then shows capability-based selection, partnership, joint IP, completed PoC and open reproducibility artifacts.",
        "not_supported": [
            "Commercial-scale adoption",
            "Success of every innovation initiative",
            "World or market leadership in AI assurance",
            "Population-wide customer outcome improvement",
        ],
        "source_boundary": "The fixed research universe records the public video and the timestamped partner-side testimony. This two-file pilot binds the source descriptor; production use should archive the transcript/video bytes and exact excerpt.",
    }


# ---------------------------------------------------------------------------
# Investigation-Admissibility Gate
# ---------------------------------------------------------------------------


def trusted_investigation_template() -> dict[str, Any]:
    return canonicalize(
        {
            "template_id": "ONZALINX_PUBLIC_ALIGNMENT_INVESTIGATION_V1",
            "version": "1.0",
            "global_requirement_kinds": list(GLOBAL_INVESTIGATION_REQUIREMENTS),
            "criterion_requirement_kinds": list(CRITERION_INVESTIGATION_REQUIREMENTS),
            "required_core_criterion_ids": list(CORE_CRITERION_IDS),
            "required_uncontrolled_route_ids": list(REQUIRED_UNCONTROLLED_ROUTE_IDS),
            "allowed_candidate_dispositions": list(ALLOWED_CANDIDATE_DISPOSITIONS),
            "closure_policy": {
                "all_mandatory_obligations_closed": True,
                "all_sources_dispositioned": True,
                "all_uncontrolled_routes_completed": True,
                "all_candidates_dispositioned": True,
                "unresolved_material_candidate_blocks_finality": True,
                "confirmed_material_core_refutation_blocks_robust": True,
                "open_world_total_completeness_claim": False,
                "ordinary_web_absence_means_false": False,
            },
        }
    )


def trusted_investigation_template_hash() -> str:
    return sha256_obj(trusted_investigation_template())


def criterion_investigation_source_matrix() -> dict[str, dict[str, tuple[str, ...]]]:
    uncontrolled = (
        "S_EN_JAPAN",
        "S_JOBTALK",
        "S_CAREERCONNECTION",
        "S_ITREVIEW",
        "S_TELNAVI",
        "S_ADVERSE_SEARCH_RECORD",
    )
    return {
        "K_CUSTOMER_OUTCOME": {
            "OFFICIAL_CLAIM": ("S_VISION", "S_BUSINESS"),
            "DIRECT_ACTION_IMPLEMENTATION": ("S_BUSINESS", "S_INTERSTOCK_FEATURE"),
            "TEMPORAL_OR_RECURRING_CONTINUITY": ("S_INTERSTOCK", "S_MARUYOSHI"),
            "INDEPENDENT_CORROBORATION": ("S_TRADE_MEDIA", "S_ITREVIEW"),
            "LIMITATION_COUNTEREVIDENCE_REVIEW": ("S_DEEP_RESEARCH", "S_CAREERCONNECTION"),
            "UNCONTROLLED_ADVERSE_SOURCE_REVIEW": uncontrolled,
        },
        "K_USER_AUTONOMY": {
            "OFFICIAL_CLAIM": ("S_MISSION", "S_INTERSTOCK"),
            "DIRECT_ACTION_IMPLEMENTATION": ("S_INTERSTOCK_POLICY", "S_CODEER", "S_MARUYOSHI"),
            "TEMPORAL_OR_RECURRING_CONTINUITY": ("S_INTERNALIZATION_2019", "S_INTERSTOCK_POLICY"),
            "INDEPENDENT_CORROBORATION": ("S_CODEER", "S_TRADE_MEDIA"),
            "LIMITATION_COUNTEREVIDENCE_REVIEW": ("S_DEEP_RESEARCH",),
            "UNCONTROLLED_ADVERSE_SOURCE_REVIEW": uncontrolled,
        },
        "K_STRUCTURAL_ROI": {
            "OFFICIAL_CLAIM": ("S_BUSINESS",),
            "DIRECT_ACTION_IMPLEMENTATION": ("S_YUKAI", "S_YUKAI_2026"),
            "TEMPORAL_OR_RECURRING_CONTINUITY": ("S_YUKAI_2018", "S_TOC_NOTE", "S_YUKAI_2026"),
            "INDEPENDENT_CORROBORATION": ("S_YUKAI_2018", "S_TRADE_MEDIA"),
            "LIMITATION_COUNTEREVIDENCE_REVIEW": ("S_DEEP_RESEARCH",),
            "UNCONTROLLED_ADVERSE_SOURCE_REVIEW": uncontrolled,
        },
        "K_CONTINUOUS_IMPROVEMENT": {
            "OFFICIAL_CLAIM": ("S_BUSINESS",),
            "DIRECT_ACTION_IMPLEMENTATION": ("S_INTERSTOCK_GROWTH", "S_INTERSTOCK_FEATURE"),
            "TEMPORAL_OR_RECURRING_CONTINUITY": ("S_INTERSTOCK_GROWTH", "S_INTERSTOCK"),
            "INDEPENDENT_CORROBORATION": ("S_TRADE_MEDIA", "S_EN_JAPAN", "S_JOBTALK"),
            "LIMITATION_COUNTEREVIDENCE_REVIEW": ("S_DEEP_RESEARCH", "S_CAREERCONNECTION"),
            "UNCONTROLLED_ADVERSE_SOURCE_REVIEW": uncontrolled,
        },
        "K_ECOSYSTEM_EXECUTION": {
            "OFFICIAL_CLAIM": ("S_PARTNER",),
            "DIRECT_ACTION_IMPLEMENTATION": ("S_AI_PARTNERSHIP", "S_AI_PATENT", "S_AI_POC", "S_AI_REPOSITORY"),
            "TEMPORAL_OR_RECURRING_CONTINUITY": ("S_AI_OUTREACH_VIDEO", "S_GHOSTDRIFT_SELECTION_NOTE", "S_AI_PATENT", "S_AI_POC"),
            "INDEPENDENT_CORROBORATION": ("S_CODEER", "S_SIGMA", "S_CEC", "S_AI_OUTREACH_VIDEO"),
            "LIMITATION_COUNTEREVIDENCE_REVIEW": ("S_DEEP_RESEARCH",),
            "UNCONTROLLED_ADVERSE_SOURCE_REVIEW": uncontrolled,
        },
    }


def build_investigation_obligations() -> tuple[InvestigationObligationRecord, ...]:
    records: list[InvestigationObligationRecord] = [
        InvestigationObligationRecord(
            "O_GLOBAL_ENTITY_DUAL_IDENTIFICATION",
            "GLOBAL",
            "ENTITY_DUAL_IDENTIFICATION",
            True,
            ("S_COMPANY_OVERVIEW", "S_GBIZ"),
            "Official company information and public-registry identity are kept as distinct provenance records.",
        ),
        InvestigationObligationRecord(
            "O_GLOBAL_SOURCE_REGISTER_DISPOSITION",
            "GLOBAL",
            "SOURCE_REGISTER_DISPOSITION",
            True,
            tuple(source.source_id for source in SOURCES),
            "Every fixed source must receive at least one declared purpose or candidate disposition.",
        ),
    ]
    matrix = criterion_investigation_source_matrix()
    for criterion_id in CORE_CRITERION_IDS:
        for requirement_kind in CRITERION_INVESTIGATION_REQUIREMENTS:
            records.append(
                InvestigationObligationRecord(
                    f"O_{criterion_id}_{requirement_kind}",
                    criterion_id,
                    requirement_kind,
                    True,
                    matrix[criterion_id][requirement_kind],
                    "Closed within the declared investigation charter; open-world total completeness is not claimed.",
                )
            )
    return tuple(records)


def build_uncontrolled_source_routes() -> tuple[UncontrolledSourceRoute, ...]:
    return (
        UncontrolledSourceRoute(
            "R_EMPLOYEE_AND_FORMER_EMPLOYEE_REVIEWS",
            "Current/former employee reviews",
            True,
            ("S_EN_JAPAN", "S_JOBTALK", "S_CAREERCONNECTION"),
            "Review company identity, date, sample size, supportive observations and tensions without treating anonymous/low-sample content as audited fact.",
            "Procedure-bounded route; no claim of exhaustive coverage of all employee speech.",
        ),
        UncontrolledSourceRoute(
            "R_PRODUCT_REVIEWS",
            "Independent product reviews",
            True,
            ("S_ITREVIEW",),
            "Review independent product-feedback candidates and preserve sample-size limitations.",
            "A one-review sample cannot establish population-level satisfaction.",
        ),
        UncontrolledSourceRoute(
            "R_PUBLIC_COMPLAINTS_AND_ATTRIBUTION",
            "Public complaints and entity attribution",
            True,
            ("S_TELNAVI", "S_COMPANY_OVERVIEW"),
            "Search complaint candidates, then compare identifiers and official contact information before attribution.",
            "Unconfirmed attribution is retained in the ledger but cannot reduce the score.",
        ),
        UncontrolledSourceRoute(
            "R_HIGH_TRUST_ADVERSE_RECORDS",
            "High-trust adverse records",
            True,
            ("S_GBIZ", "S_ADVERSE_SEARCH_RECORD"),
            "Use the legal name and corporate number in a declared query plan for administrative sanctions, litigation and major incidents.",
            "No confirmed match within the plan is not proof that no adverse fact exists anywhere.",
        ),
    )


def build_adverse_candidate_reviews() -> tuple[AdverseCandidateReview, ...]:
    return (
        AdverseCandidateReview(
            "C_EN_JAPAN",
            "S_EN_JAPAN",
            "EMPLOYEE_REVIEW",
            "LIMITED_SAMPLE",
            "ENTITY_MATCH_CONFIRMED",
            "NON_MATERIAL_CONTEXT",
            "ADMITTED_SUPPORT_CONTEXT_ONLY",
            False,
            False,
            "Supportive observations and business-differentiation tensions are retained as context; no score uplift.",
        ),
        AdverseCandidateReview(
            "C_JOBTALK",
            "S_JOBTALK",
            "FORMER_EMPLOYEE_REVIEW",
            "SINGLE_REVIEW",
            "ENTITY_MATCH_CONFIRMED",
            "NON_MATERIAL_CONTEXT",
            "ADMITTED_SUPPORT_CONTEXT_ONLY",
            False,
            False,
            "One historical former-employee review; no company-wide inference and no score uplift.",
        ),
        AdverseCandidateReview(
            "C_CAREERCONNECTION",
            "S_CAREERCONNECTION",
            "WORKPLACE_TENSION",
            "SINGLE_CONTRIBUTOR",
            "ENTITY_MATCH_CONFIRMED",
            "NON_MATERIAL_TENSION",
            "ADMITTED_TENSION_CONTEXT_ONLY",
            False,
            False,
            "Retained as a limitation on organization-wide integrity/workplace assurances; not imported into the five core scores.",
        ),
        AdverseCandidateReview(
            "C_ITREVIEW",
            "S_ITREVIEW",
            "PRODUCT_REVIEW",
            "SINGLE_REVIEW",
            "PRODUCT_MATCH_CONFIRMED",
            "NON_MATERIAL_CONTEXT",
            "ADMITTED_SUPPORT_CONTEXT_ONLY",
            False,
            False,
            "Too small a sample for score uplift or population-level satisfaction claims.",
        ),
        AdverseCandidateReview(
            "C_TELNAVI",
            "S_TELNAVI",
            "PUBLIC_COMPLAINT",
            "LOW_RELIABILITY_MIXED_CONTENT",
            "ENTITY_ATTRIBUTION_UNCONFIRMED",
            "POTENTIALLY_MATERIAL_IF_ATTRIBUTED",
            "REJECTED_ENTITY_ATTRIBUTION_UNCONFIRMED",
            False,
            False,
            "The listed number is not on the official company page and some posts describe unrelated services; candidate retained but not attributed.",
        ),
        AdverseCandidateReview(
            "C_HIGH_TRUST_ADVERSE_SEARCH",
            "S_ADVERSE_SEARCH_RECORD",
            "ADMINISTRATIVE_LITIGATION_INCIDENT_SEARCH",
            "PROCEDURE_BOUNDED_HIGH_TRUST_SEARCH",
            "NO_CONFIRMED_ENTITY_MATCH",
            "MATERIAL_IF_CONFIRMED",
            "NO_CONFIRMED_MATCH_IN_DECLARED_QUERY_PLAN",
            False,
            False,
            "No confirmed matching record was found within the declared plan; absence is not converted into positive evidence.",
        ),
    )


def derive_source_dispositions(
    obligations: Sequence[InvestigationObligationRecord],
    routes: Sequence[UncontrolledSourceRoute],
    candidates: Sequence[AdverseCandidateReview],
) -> tuple[SourceDispositionRecord, ...]:
    purposes: dict[str, set[str]] = {source.source_id: set() for source in SOURCES}
    for claim in CLAIMS:
        for source_id in claim.source_ids:
            purposes[source_id].add("CLAIM_BASIS")
    for artifact in ARTIFACTS:
        for source_id in artifact.source_ids:
            purposes[source_id].add("EVIDENCE_BASIS")
    for obligation in obligations:
        for source_id in obligation.source_ids:
            purposes[source_id].add(f"INVESTIGATION:{obligation.requirement_kind}")
    for route in routes:
        for source_id in route.source_ids:
            purposes[source_id].add(f"UNCONTROLLED_ROUTE:{route.route_id}")
    for candidate in candidates:
        purposes[candidate.source_id].add(f"CANDIDATE:{candidate.disposition}")
    return tuple(
        SourceDispositionRecord(
            source_id,
            "PURPOSE_ASSIGNED" if purposes[source_id] else "UNASSIGNED",
            tuple(sorted(purposes[source_id])),
        )
        for source_id in sorted(purposes)
    )


def build_investigation_assurance() -> dict[str, Any]:
    obligations = build_investigation_obligations()
    routes = build_uncontrolled_source_routes()
    candidates = build_adverse_candidate_reviews()
    source_dispositions = derive_source_dispositions(obligations, routes, candidates)
    records_payload = {
        "obligations": obligations,
        "source_dispositions": source_dispositions,
        "uncontrolled_source_routes": routes,
        "adverse_candidate_reviews": candidates,
    }
    return canonicalize(
        {
            "trusted_template": trusted_investigation_template(),
            "trusted_template_hash": trusted_investigation_template_hash(),
            **records_payload,
            "source_register_hash": sha256_obj(SOURCES),
            "review_records_hash": sha256_obj(records_payload),
        }
    )


def validate_investigation_gate(manifest: Mapping[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    assurance = manifest.get("investigation_assurance")
    if not isinstance(assurance, Mapping):
        return {
            "status": STATUS_INVESTIGATION_INCOMPLETE,
            "passed": False,
            "errors": ["investigation_assurance is missing or not an object"],
        }

    template = assurance.get("trusted_template")
    claimed_template_hash = assurance.get("trusted_template_hash")
    expected_template_hash = trusted_investigation_template_hash()
    if sha256_obj(template) != expected_template_hash or claimed_template_hash != expected_template_hash:
        errors.append("investigation template is not the trusted out-of-band template")

    source_ids = {source["source_id"] for source in manifest["sources"]}
    obligation_values = assurance.get("obligations", [])
    obligations = tuple(
        InvestigationObligationRecord(
            item["obligation_id"],
            item["scope_id"],
            item["requirement_kind"],
            item["closed"],
            tuple(item["source_ids"]),
            item["notes"],
        )
        for item in obligation_values
    )
    expected_obligation_ids = {
        "O_GLOBAL_ENTITY_DUAL_IDENTIFICATION",
        "O_GLOBAL_SOURCE_REGISTER_DISPOSITION",
        *(
            f"O_{criterion_id}_{requirement_kind}"
            for criterion_id in CORE_CRITERION_IDS
            for requirement_kind in CRITERION_INVESTIGATION_REQUIREMENTS
        ),
    }
    actual_obligation_ids = [item.obligation_id for item in obligations]
    if len(actual_obligation_ids) != len(set(actual_obligation_ids)):
        errors.append("duplicate investigation obligation identifier")
    if set(actual_obligation_ids) != expected_obligation_ids:
        errors.append("mandatory investigation obligation universe is incomplete or expanded")
    expected_obligations = {item.obligation_id: item for item in build_investigation_obligations()}
    for obligation in obligations:
        expected = expected_obligations.get(obligation.obligation_id)
        if expected is not None and (
            obligation.scope_id != expected.scope_id
            or obligation.requirement_kind != expected.requirement_kind
            or tuple(obligation.source_ids) != tuple(expected.source_ids)
        ):
            errors.append(f"mandatory obligation structure differs from trusted template: {obligation.obligation_id}")
        if not obligation.closed:
            errors.append(f"mandatory obligation not closed: {obligation.obligation_id}")
        if not obligation.source_ids:
            errors.append(f"mandatory obligation lacks sources: {obligation.obligation_id}")
        unknown = set(obligation.source_ids) - source_ids
        if unknown:
            errors.append(f"mandatory obligation references unknown sources: {obligation.obligation_id}:{sorted(unknown)}")

    disposition_values = assurance.get("source_dispositions", [])
    source_dispositions = tuple(
        SourceDispositionRecord(item["source_id"], item["status"], tuple(item["purposes"]))
        for item in disposition_values
    )
    disposition_ids = [item.source_id for item in source_dispositions]
    if len(disposition_ids) != len(set(disposition_ids)):
        errors.append("duplicate source disposition identifier")
    if set(disposition_ids) != source_ids:
        errors.append("fixed source register is not fully dispositioned")
    if any(item.status != "PURPOSE_ASSIGNED" or not item.purposes for item in source_dispositions):
        errors.append("one or more fixed sources lack a declared purpose")
    expected_dispositions = {
        item.source_id: item
        for item in derive_source_dispositions(
            build_investigation_obligations(),
            build_uncontrolled_source_routes(),
            build_adverse_candidate_reviews(),
        )
    }
    for item in source_dispositions:
        expected = expected_dispositions.get(item.source_id)
        if expected is not None and (item.status != expected.status or tuple(item.purposes) != tuple(expected.purposes)):
            errors.append(f"source disposition differs from the fixed purpose register: {item.source_id}")
    expected_source_hash = sha256_obj(SOURCES)
    if (
        assurance.get("source_register_hash") != sha256_obj(manifest["sources"])
        or assurance.get("source_register_hash") != expected_source_hash
    ):
        errors.append("fixed source register hash mismatch")

    route_values = assurance.get("uncontrolled_source_routes", [])
    routes = tuple(
        UncontrolledSourceRoute(
            item["route_id"],
            item["label"],
            item["completed"],
            tuple(item["source_ids"]),
            item["query_scope"],
            item["notes"],
        )
        for item in route_values
    )
    route_ids = [item.route_id for item in routes]
    if len(route_ids) != len(set(route_ids)):
        errors.append("duplicate uncontrolled-source route identifier")
    if set(route_ids) != set(REQUIRED_UNCONTROLLED_ROUTE_IDS):
        errors.append("required uncontrolled-source routes are incomplete or expanded")
    expected_routes = {item.route_id: item for item in build_uncontrolled_source_routes()}
    for route in routes:
        expected = expected_routes.get(route.route_id)
        if expected is not None and (
            route.label != expected.label
            or tuple(route.source_ids) != tuple(expected.source_ids)
            or route.query_scope != expected.query_scope
        ):
            errors.append(f"uncontrolled-source route structure differs from trusted template: {route.route_id}")
        if not route.completed:
            errors.append(f"uncontrolled-source route not completed: {route.route_id}")
        if not route.source_ids or set(route.source_ids) - source_ids:
            errors.append(f"uncontrolled-source route has invalid sources: {route.route_id}")

    candidate_values = assurance.get("adverse_candidate_reviews", [])
    candidates = tuple(
        AdverseCandidateReview(
            item["candidate_id"],
            item["source_id"],
            item["category"],
            item["reliability"],
            item["attribution_status"],
            item["materiality"],
            item["disposition"],
            item["unresolved"],
            item["material_core_refutation"],
            item["notes"],
        )
        for item in candidate_values
    )
    candidate_ids = [item.candidate_id for item in candidates]
    if len(candidate_ids) != len(set(candidate_ids)):
        errors.append("duplicate adverse candidate identifier")
    expected_candidates = {item.candidate_id: item for item in build_adverse_candidate_reviews()}
    if set(candidate_ids) != set(expected_candidates):
        errors.append("adverse candidate ledger identifiers differ from the fixed candidate universe")
    for candidate in candidates:
        expected = expected_candidates.get(candidate.candidate_id)
        if expected is not None and (
            candidate.source_id != expected.source_id
            or candidate.category != expected.category
            or candidate.reliability != expected.reliability
        ):
            errors.append(f"adverse candidate identity differs from the fixed ledger: {candidate.candidate_id}")
        if candidate.source_id not in source_ids:
            errors.append(f"adverse candidate references unknown source: {candidate.candidate_id}")
        if candidate.disposition not in ALLOWED_CANDIDATE_DISPOSITIONS:
            errors.append(f"adverse candidate lacks an allowed disposition: {candidate.candidate_id}")
        admitted_material = candidate.disposition == "ADMITTED_MATERIAL_CORE_REFUTATION"
        if candidate.material_core_refutation != admitted_material:
            errors.append(f"material-refutation flag/disposition mismatch: {candidate.candidate_id}")
        if admitted_material and (
            candidate.unresolved
            or candidate.materiality not in {"MATERIAL", "MATERIAL_IF_CONFIRMED"}
            or "UNCONFIRMED" in candidate.attribution_status
            or candidate.attribution_status.startswith("NO_CONFIRMED")
        ):
            errors.append(f"admitted material refutation lacks confirmed material attribution: {candidate.candidate_id}")

    review_records_payload = {
        "obligations": assurance.get("obligations", []),
        "source_dispositions": assurance.get("source_dispositions", []),
        "uncontrolled_source_routes": assurance.get("uncontrolled_source_routes", []),
        "adverse_candidate_reviews": assurance.get("adverse_candidate_reviews", []),
    }
    if assurance.get("review_records_hash") != sha256_obj(review_records_payload):
        errors.append("investigation review records hash mismatch")

    unresolved_material = tuple(
        item.candidate_id
        for item in candidates
        if item.unresolved and item.materiality in {"MATERIAL", "MATERIAL_IF_CONFIRMED", "POTENTIALLY_MATERIAL_IF_ATTRIBUTED"}
    )
    confirmed_material_refutations = tuple(
        item.candidate_id
        for item in candidates
        if item.material_core_refutation and item.disposition == "ADMITTED_MATERIAL_CORE_REFUTATION"
    )
    non_material_tensions = tuple(
        item.candidate_id
        for item in candidates
        if item.disposition == "ADMITTED_TENSION_CONTEXT_ONLY" and not item.material_core_refutation
    )

    mandatory_total = len(expected_obligation_ids)
    mandatory_closed = sum(1 for item in obligations if item.closed and item.obligation_id in expected_obligation_ids)
    source_total = len(source_ids)
    source_dispositioned = sum(1 for item in source_dispositions if item.status == "PURPOSE_ASSIGNED" and item.purposes)
    routes_closed = sum(1 for item in routes if item.completed)
    candidates_dispositioned = sum(1 for item in candidates if item.disposition in ALLOWED_CANDIDATE_DISPOSITIONS)

    blocking_status = None
    if errors or unresolved_material:
        blocking_status = STATUS_INVESTIGATION_INCOMPLETE
    elif confirmed_material_refutations:
        blocking_status = STATUS_MATERIAL_COUNTEREVIDENCE_CONFIRMED
    passed = blocking_status is None

    return {
        "status": INVESTIGATION_CLOSED if passed else blocking_status,
        "passed": passed,
        "trusted_template_hash": expected_template_hash,
        "mandatory_total": mandatory_total,
        "mandatory_closed": mandatory_closed,
        "source_register_total": source_total,
        "source_register_dispositioned": source_dispositioned,
        "core_criterion_total": len(CORE_CRITERION_IDS),
        "core_criterion_closed": sum(
            1
            for criterion_id in CORE_CRITERION_IDS
            if all(
                f"O_{criterion_id}_{requirement_kind}" in actual_obligation_ids
                and next(
                    item.closed
                    for item in obligations
                    if item.obligation_id == f"O_{criterion_id}_{requirement_kind}"
                )
                for requirement_kind in CRITERION_INVESTIGATION_REQUIREMENTS
            )
        ) if set(actual_obligation_ids) >= {
            f"O_{criterion_id}_{requirement_kind}"
            for criterion_id in CORE_CRITERION_IDS
            for requirement_kind in CRITERION_INVESTIGATION_REQUIREMENTS
        } else 0,
        "uncontrolled_route_total": len(REQUIRED_UNCONTROLLED_ROUTE_IDS),
        "uncontrolled_route_closed": routes_closed,
        "candidate_total": len(candidates),
        "candidate_dispositioned": candidates_dispositioned,
        "confirmed_material_core_refutations": list(confirmed_material_refutations),
        "unresolved_material_candidates": list(unresolved_material),
        "non_material_tensions_retained": list(non_material_tensions),
        "open_world_total_completeness": "NOT_CLAIMED",
        "errors": sorted(set(errors)),
    }


# ---------------------------------------------------------------------------
# Manifest, prospective freeze, derived result, and certificate
# ---------------------------------------------------------------------------


def build_manifest() -> dict[str, Any]:
    return canonicalize(
        {
            "metadata": evaluation_metadata(),
            "source_hash_policy": source_hash_policy(),
            "evidence_level_scale": evidence_level_scale(),
            "sources": SOURCES,
            "investigation_assurance": build_investigation_assurance(),
            "claims": CLAIMS,
            "criteria": CRITERIA,
            "artifacts": ARTIFACTS,
            "mapping_profiles": MAPPING_PROFILES,
            "weight_vertices": BASE_CORE_WEIGHTS + EXTENDED_WEIGHTS,
            "threshold_profiles": THRESHOLDS,
            "reference_frames": REFERENCE_FRAMES,
            "future_milestones_not_scored": FUTURE_MILESTONES,
            "restrictions": evaluation_restrictions(),
        }
    )


def prospective_charter_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    # Evidence already observed before the freeze is intentionally excluded from
    # the prospective commitment payload. The payload fixes the claim snapshot,
    # dimensions, mapping profiles, weights, thresholds, reference frame and rules
    # for evaluating later observations.
    return {
        "snapshot_date": manifest["metadata"]["snapshot_date"],
        "assessment_mode": "PROSPECTIVE_CHARTER_READY_FOR_EXTERNAL_TIMESTAMP",
        "claims": manifest["claims"],
        "criteria": manifest["criteria"],
        "mapping_profiles": manifest["mapping_profiles"],
        "weight_vertices": [
            item for item in manifest["weight_vertices"]
            if set(key for key, _ in item["criterion_weights"]) == set(CORE_CRITERION_IDS)
        ],
        "threshold_profiles": [
            item for item in manifest["threshold_profiles"]
            if item["group"] in {"CORE_COARSE", "CORE_FINE"}
        ],
        "reference_frames": manifest["reference_frames"],
        "restrictions": manifest["restrictions"],
        "investigation_template": manifest["investigation_assurance"]["trusted_template"],
        "investigation_gate_rule": "A future numerical result is final only after all mandatory investigation obligations and uncontrolled-source routes are closed, every candidate is dispositioned, no material candidate is unresolved, and no confirmed material core refutation is admitted.",
        "future_observation_rule": "Only evidence with an observed/published time later than an externally timestamped commitment is eligible for the prospective run.",
    }


def objects_from_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "sources": parse_sources(manifest["sources"]),
        "claims": parse_claims(manifest["claims"]),
        "criteria": parse_criteria(manifest["criteria"]),
        "artifacts": parse_artifacts(manifest["artifacts"]),
        "mapping_profiles": parse_mapping_profiles(manifest["mapping_profiles"]),
        "weight_vertices": parse_weight_vertices(manifest["weight_vertices"]),
        "threshold_profiles": parse_threshold_profiles(manifest["threshold_profiles"]),
        "reference_frames": parse_reference_frames(manifest["reference_frames"]),
    }


def evaluate_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    if "investigation_assurance" not in manifest:
        return {
            "status": STATUS_INVESTIGATION_INCOMPLETE,
            "investigation_gate": {
                "status": STATUS_INVESTIGATION_INCOMPLETE,
                "passed": False,
                "errors": ["investigation_assurance is missing"],
            },
            "numeric_evaluation_finality": False,
            "core_frontier": None,
            "core_coarse": None,
        }
    errors = validate_manifest(manifest)
    if errors:
        return {"status": DecisionStatus.INVALID.value, "validation_errors": errors}

    try:
        investigation_gate = validate_investigation_gate(manifest)
    except (KeyError, TypeError, ValueError) as exc:
        investigation_gate = {
            "status": STATUS_INVESTIGATION_INCOMPLETE,
            "passed": False,
            "errors": [f"malformed investigation assurance: {exc}"],
        }
    if not investigation_gate["passed"]:
        return {
            "status": investigation_gate["status"],
            "investigation_gate": investigation_gate,
            "numeric_evaluation_finality": False,
            "core_frontier": None,
            "core_coarse": None,
            "assurance_boundary": {
                "guaranteed": [
                    "The numerical evaluation cannot be finalized unless the investigation gate passes."
                ],
                "not_guaranteed": [
                    "A robust public-alignment conclusion while mandatory research is incomplete, a material candidate is unresolved, or material core counterevidence is confirmed."
                ],
            },
        }

    objects = objects_from_manifest(manifest)
    core_vertices = tuple(
        item for item in objects["weight_vertices"]
        if set(item.weights()) == set(CORE_CRITERION_IDS)
    )
    extended_vertices = tuple(
        item for item in objects["weight_vertices"]
        if set(item.weights()) == set(EXTENDED_CRITERION_IDS)
    )
    core_coarse = evaluate_universe(
        criterion_ids=CORE_CRITERION_IDS,
        artifacts=objects["artifacts"],
        mapping_profiles=objects["mapping_profiles"],
        weight_vertices=core_vertices,
        threshold_profiles=core_threshold_profiles(objects["threshold_profiles"], "CORE_COARSE"),
        reference_frames=objects["reference_frames"],
    )
    core_frontier_lower = D(core_coarse["threshold_frontier"]["guaranteed_lower_score"])
    core_frontier = {
        "status": "ROBUST_LOWER_BOUND_CERTIFIED",
        "guaranteed_lower_score": decimal_to_str(core_frontier_lower),
        "possible_upper_score": core_coarse["threshold_frontier"]["possible_upper_score"],
        "robust_pass_threshold_range": {
            "minimum": "0",
            "maximum_inclusive": decimal_to_str(core_frontier_lower),
        },
        "strict_establishment_line": STRICT_ESTABLISHMENT_LINE,
        "strict_margin": decimal_to_str(core_frontier_lower - D(STRICT_ESTABLISHMENT_LINE)),
        "declared_threshold_tests": {
            "55": core_frontier_lower >= D("55"),
            "60": core_frontier_lower >= D("60"),
            "68": core_frontier_lower >= D(STRICT_ESTABLISHMENT_LINE),
            "70": core_frontier_lower >= D("70"),
            "75": core_frontier_lower >= D("75"),
        },
        "interpretation": "The threshold frontier is the primary result. The strict establishment line is 68; categorical labels remain dependent on the committed governance thresholds.",
    }
    core_fine = evaluate_universe(
        criterion_ids=CORE_CRITERION_IDS,
        artifacts=objects["artifacts"],
        mapping_profiles=objects["mapping_profiles"],
        weight_vertices=core_vertices,
        threshold_profiles=core_threshold_profiles(objects["threshold_profiles"], "CORE_FINE"),
        reference_frames=objects["reference_frames"],
    )
    extended = evaluate_universe(
        criterion_ids=EXTENDED_CRITERION_IDS,
        artifacts=objects["artifacts"],
        mapping_profiles=objects["mapping_profiles"],
        weight_vertices=extended_vertices,
        threshold_profiles=core_threshold_profiles(objects["threshold_profiles"], "EXTENDED"),
        reference_frames=objects["reference_frames"],
    )
    deletion = evidence_deletion_analysis(objects)
    criterion_loo = criterion_leave_one_out_analysis(objects)
    diagnostics = criterion_diagnostics(CORE_CRITERION_IDS + EXTENDED_CRITERION_IDS, objects["artifacts"], objects["mapping_profiles"])
    prospective_payload = prospective_charter_payload(manifest)
    philosophy_chains = philosophy_to_implementation_chains(objects["sources"])
    extended_individual = individual_extended_frontiers(objects)

    # Active label fields are deliberately excluded from every numerical path.
    label_invariance = True

    return {
        "status": STATUS_VALID_RETROSPECTIVE_EVALUATION,
        "investigation_gate": investigation_gate,
        "numeric_evaluation_finality": True,
        "core_frontier": core_frontier,
        "core_coarse": core_coarse,
        "core_fine": core_fine,
        "extended_values": extended,
        "criterion_diagnostics": diagnostics,
        "evidence_cluster_deletion": deletion,
        "evidence_group_deletion": evidence_group_deletion_analysis(objects),
        "criterion_leave_one_out": criterion_loo,
        "ai_assurance_witness": ai_assurance_witness(objects["artifacts"]),
        "philosophy_to_implementation_chains": philosophy_chains,
        "extended_individual_frontiers": extended_individual,
        "future_milestones_not_scored": list(FUTURE_MILESTONES),
        "label_invariance": label_invariance,
        "prospective_charter": {
            "ready_for_external_timestamp": True,
            "external_timestamp_verified": False,
            "payload_hash": sha256_obj(prospective_payload),
            "payload": prospective_payload,
        },
        "assurance_boundary": {
            "guaranteed": [
                "The evaluator-target relationship and the fact that this is not an independent third-party audit are disclosed in the machine-readable manifest.",
                "Every evidence interval is a human-authored, source-bound integer ordinal input with a public description, independence class and stated limitations.",
                "The trusted investigation template, all 32 mandatory obligations, all four uncontrolled-source routes and all candidate dispositions passed before the numerical result was finalized.",
                "After the declared inputs were fixed, every mapping profile, core criterion-weight vertex, threshold profile, reference frame and rectangular evidence completion was included in the reported closure.",
                "The threshold frontier is the minimum score lower bound across the complete declared family universe.",
                "Evidence-cluster deletion and criterion leave-one-out analyses are deterministically recomputable.",
                "The certificate can be semantically replayed from its embedded inputs.",
            ],
            "not_guaranteed": [
                "Independent third-party audit status or evaluator neutrality.",
                "Unique or objectively compelled correctness of each human-authored evidence interval.",
                "Moral, legal or policy correctness of the company values.",
                "Truth of remote public statements beyond the declared source-integrity assumptions.",
                "Coverage of evidence omitted from the public research universe.",
                "Prospective temporal blind commitment for this retrospective result.",
                "Trusted time, signer identity or non-repudiation without external services.",
                "Company-wide customer success, realized ROI, employee conduct or commercial-scale AI-assurance adoption.",
            ],
        },
    }


def seal_certificate(payload: Mapping[str, Any]) -> dict[str, Any]:
    sealed = copy.deepcopy(dict(payload))
    sealed.pop("certificate_payload_hash", None)
    sealed["certificate_payload_hash"] = sha256_obj(sealed)
    return sealed


def verify_certificate_hash(certificate: Mapping[str, Any]) -> tuple[bool, str, str]:
    claimed = str(certificate.get("certificate_payload_hash", ""))
    payload = copy.deepcopy(dict(certificate))
    payload.pop("certificate_payload_hash", None)
    actual = sha256_obj(payload)
    return claimed == actual and is_sha256_hex(claimed), claimed, actual


def build_certificate() -> dict[str, Any]:
    manifest = build_manifest()
    derived = evaluate_manifest(manifest)
    payload = {
        "schema": CERTIFICATE_SCHEMA,
        "certificate_type": "NON_ARBITRARINESS_PUBLIC_CLAIM_TO_EVIDENCE_CERTIFICATE",
        "engine": {
            "name": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "code_hash": module_code_hash(),
            "python_minimum": "3.11",
            "standard_library_only": True,
        },
        "inputs": manifest,
        "derived": derived,
        "commitments": {
            "inputs_hash": sha256_obj(manifest),
            "derived_hash": sha256_obj(derived),
            "research_basis_hash": DEEP_RESEARCH_SHA256,
            "fixed_evaluation_universe_hash": trusted_evaluation_universe_hash(),
            "trusted_investigation_template_hash": manifest["investigation_assurance"]["trusted_template_hash"],
            "fixed_source_register_hash": manifest["investigation_assurance"]["source_register_hash"],
            "investigation_review_records_hash": manifest["investigation_assurance"]["review_records_hash"],
            "prospective_charter_hash": derived.get("prospective_charter", {}).get("payload_hash"),
        },
        "security_boundary": {
            "deterministic_content_binding": True,
            "semantic_replay_supported": True,
            "trusted_external_timestamp": False,
            "public_key_signature": False,
            "remote_source_page_bytes_bundled": False,
            "evaluator_relationship_disclosed": True,
            "independent_third_party_audit": False,
            "human_evidence_interval_assignment_disclosed": True,
            "evidence_interval_unique_correctness_claimed": False,
            "investigation_gate_enforced_before_final_numeric_decision": True,
        },
    }
    return seal_certificate(canonicalize(payload))


def semantic_replay_certificate(certificate: Mapping[str, Any]) -> tuple[bool, list[str], Optional[dict[str, Any]]]:
    errors: list[str] = []
    hash_ok, claimed, actual = verify_certificate_hash(certificate)
    if not hash_ok:
        errors.append(f"certificate payload hash mismatch: claimed={claimed} actual={actual}")
    if certificate.get("schema") != CERTIFICATE_SCHEMA:
        errors.append("unsupported certificate schema")
    engine = certificate.get("engine", {})
    if engine.get("name") != ENGINE_NAME or engine.get("version") != ENGINE_VERSION:
        errors.append("engine identity mismatch")
    if engine.get("code_hash") != module_code_hash():
        errors.append("executing code hash differs from certificate engine code hash")
    try:
        inputs = certificate["inputs"]
        replayed = evaluate_manifest(inputs)
        expected_commitments = {
            "inputs_hash": sha256_obj(inputs),
            "derived_hash": sha256_obj(replayed),
            "research_basis_hash": DEEP_RESEARCH_SHA256,
            "fixed_evaluation_universe_hash": trusted_evaluation_universe_hash(),
            "trusted_investigation_template_hash": inputs["investigation_assurance"]["trusted_template_hash"],
            "fixed_source_register_hash": inputs["investigation_assurance"]["source_register_hash"],
            "investigation_review_records_hash": inputs["investigation_assurance"]["review_records_hash"],
            "prospective_charter_hash": replayed.get("prospective_charter", {}).get("payload_hash"),
        }
        if canonicalize(replayed) != canonicalize(certificate.get("derived")):
            errors.append("semantic replay derived payload mismatch")
        if canonicalize(expected_commitments) != canonicalize(certificate.get("commitments")):
            errors.append("component commitment mismatch")
        return not errors, errors, replayed
    except Exception as exc:  # pragma: no cover - defensive certificate parser boundary
        errors.append(f"semantic replay failed: {exc}")
        return False, errors, None


# ---------------------------------------------------------------------------
# Human output
# ---------------------------------------------------------------------------


def compact_summary(derived: Mapping[str, Any]) -> dict[str, Any]:
    if derived.get("status") != STATUS_VALID_RETROSPECTIVE_EVALUATION:
        return {
            "status": derived.get("status"),
            "investigation_gate": derived.get("investigation_gate"),
            "numeric_evaluation_finality": derived.get("numeric_evaluation_finality", False),
        }
    core = derived["core_coarse"]
    fine = derived["core_fine"]
    extended = derived["extended_values"]
    return {
        "assessment_mode": ASSESSMENT_MODE,
        "investigation_gate": derived["investigation_gate"],
        "core_frontier": derived["core_frontier"],
        "core_coarse": {
            "status": core["status"],
            "possible_outcomes": core["possible_outcomes"],
            "robust_outcome": core["robust_outcome"],
            "score_envelope": core["score_envelope"],
            "threshold_frontier": core["threshold_frontier"],
            "family_count": core["family_count"],
        },
        "core_fine": {
            "status": fine["status"],
            "possible_outcomes": fine["possible_outcomes"],
            "score_envelope": fine["score_envelope"],
        },
        "extended_values": {
            "status": extended["status"],
            "possible_outcomes": extended["possible_outcomes"],
            "score_envelope": extended["score_envelope"],
        },
        "ai_assurance_witness": derived["ai_assurance_witness"],
        "evidence_group_deletion": derived["evidence_group_deletion"],
        "philosophy_to_implementation_chains": derived["philosophy_to_implementation_chains"],
        "extended_individual_frontiers": derived["extended_individual_frontiers"],
        "future_milestones_not_scored": derived["future_milestones_not_scored"],
        "prospective_charter_hash": derived["prospective_charter"]["payload_hash"],
        "label_invariance": derived["label_invariance"],
    }


def print_evaluation_summary(certificate: Mapping[str, Any]) -> None:
    derived = certificate["derived"]
    summary = compact_summary(derived)
    frontier = summary["core_frontier"]
    core = summary["core_coarse"]
    fine = summary["core_fine"]
    extended = summary["extended_values"]
    print(f"{ENGINE_NAME} {ENGINE_VERSION}")
    print(f"assessment_mode: {ASSESSMENT_MODE}")
    gate = summary["investigation_gate"]
    print(f"investigation_gate_status: {gate['status']}")
    if not summary.get("numeric_evaluation_finality", True):
        print("numeric_evaluation_finality: False")
        for error in gate.get("errors", []):
            print(f"investigation_gate_error: {error}")
        return
    print(f"mandatory_investigation_obligations: {gate['mandatory_closed']}/{gate['mandatory_total']}")
    print(f"fixed_source_register: {gate['source_register_dispositioned']}/{gate['source_register_total']}")
    print(f"uncontrolled_source_routes: {gate['uncontrolled_route_closed']}/{gate['uncontrolled_route_total']}")
    print(f"adverse_candidates_dispositioned: {gate['candidate_dispositioned']}/{gate['candidate_total']}")
    print(f"primary_frontier_status: {frontier['status']}")
    print(f"primary_guaranteed_lower_score: {frontier['guaranteed_lower_score']}")
    print(f"declared_threshold_tests: {frontier['declared_threshold_tests']}")
    print(f"core_coarse_status: {core['status']}")
    print(f"core_coarse_possible_outcomes: {core['possible_outcomes']}")
    print(f"core_score_envelope: {core['score_envelope']}")
    print(f"core_guaranteed_lower_score: {core['threshold_frontier']['guaranteed_lower_score']}")
    print(f"core_family_count: {core['family_count']}")
    print(f"core_fine_status: {fine['status']}")
    print(f"core_fine_possible_outcomes: {fine['possible_outcomes']}")
    print(f"extended_assurance_status: {extended['status']}")
    print(f"extended_assurance_possible_outcomes: {extended['possible_outcomes']}")
    print(f"ai_assurance_witness: {summary['ai_assurance_witness']['witness_outcome']}")
    print(f"prospective_charter_hash: {summary['prospective_charter_hash']}")
    print(f"certificate_payload_hash: {certificate['certificate_payload_hash']}")


# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------


def ast_contains_float_constant(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return any(isinstance(node, ast.Constant) and isinstance(node.value, float) for node in ast.walk(tree))


def run_self_tests() -> int:
    tests = 0
    manifest = build_manifest()
    errors = validate_manifest(manifest)
    assert not errors, errors
    assert manifest["metadata"]["snapshot_date"] == "2026-08-18"
    assert manifest["metadata"]["evaluator_entity_name"] == "株式会社GhostDrift数理研究所"
    assert manifest["metadata"]["independent_third_party_audit_claimed"] is False
    assert manifest["evidence_level_scale"]["assignment_policy"]["machine_derived"] is False
    assert manifest["evidence_level_scale"]["assignment_policy"]["unique_correctness_claimed"] is False
    disclosure_tampered = copy.deepcopy(manifest)
    disclosure_tampered["metadata"]["independent_third_party_audit_claimed"] = True
    assert evaluate_manifest(disclosure_tampered)["status"] == DecisionStatus.INVALID.value
    tests += 1
    assert len(manifest["sources"]) == 38
    core_lines = sorted(
        D(band["minimum_score"])
        for profile in manifest["threshold_profiles"]
        if profile["group"] == "CORE_COARSE"
        for band in profile["bands"]
        if band["outcome"] == "PUBLIC_ALIGNMENT_ESTABLISHED"
    )
    assert core_lines == [D("55"), D("60"), D("68")]
    assert sha256_obj(manifest_evaluation_universe_payload(manifest)) == trusted_evaluation_universe_hash()
    universe_tampered = copy.deepcopy(manifest)
    universe_tampered["sources"][0]["title"] = "tampered source title"
    assert evaluate_manifest(universe_tampered)["status"] == DecisionStatus.INVALID.value
    tests += 1

    assert not ast_contains_float_constant(Path(__file__)), "binary float literal found in code"
    tests += 1

    criteria_ids = {item["criterion_id"] for item in manifest["criteria"]}
    assert "K_NOVEL_DOMAIN_EXECUTION" not in criteria_ids
    tests += 1

    derived = evaluate_manifest(manifest)
    assert derived["status"] == STATUS_VALID_RETROSPECTIVE_EVALUATION
    missing_gate_manifest = copy.deepcopy(manifest)
    del missing_gate_manifest["investigation_assurance"]
    assert evaluate_manifest(missing_gate_manifest)["status"] == STATUS_INVESTIGATION_INCOMPLETE
    tests += 1

    gate = derived["investigation_gate"]
    assert gate["status"] == INVESTIGATION_CLOSED
    assert gate["mandatory_closed"] == gate["mandatory_total"] == 32
    assert gate["source_register_dispositioned"] == gate["source_register_total"] == 38
    assert gate["uncontrolled_route_closed"] == gate["uncontrolled_route_total"] == 4
    assert gate["candidate_dispositioned"] == gate["candidate_total"] == 6
    tests += 1

    missing_obligation_manifest = copy.deepcopy(manifest)
    missing_obligation_manifest["investigation_assurance"]["obligations"].pop()
    records_payload = {
        "obligations": missing_obligation_manifest["investigation_assurance"]["obligations"],
        "source_dispositions": missing_obligation_manifest["investigation_assurance"]["source_dispositions"],
        "uncontrolled_source_routes": missing_obligation_manifest["investigation_assurance"]["uncontrolled_source_routes"],
        "adverse_candidate_reviews": missing_obligation_manifest["investigation_assurance"]["adverse_candidate_reviews"],
    }
    missing_obligation_manifest["investigation_assurance"]["review_records_hash"] = sha256_obj(records_payload)
    assert evaluate_manifest(missing_obligation_manifest)["status"] == STATUS_INVESTIGATION_INCOMPLETE
    malformed_gate_manifest = copy.deepcopy(manifest)
    malformed_gate_manifest["investigation_assurance"]["obligations"] = [{"bad": True}]
    malformed_result = evaluate_manifest(malformed_gate_manifest)
    assert malformed_result["status"] == STATUS_INVESTIGATION_INCOMPLETE
    assert compact_summary(malformed_result)["numeric_evaluation_finality"] is False
    tests += 1

    incomplete_route_manifest = copy.deepcopy(manifest)
    incomplete_route_manifest["investigation_assurance"]["uncontrolled_source_routes"][0]["completed"] = False
    records_payload = {
        "obligations": incomplete_route_manifest["investigation_assurance"]["obligations"],
        "source_dispositions": incomplete_route_manifest["investigation_assurance"]["source_dispositions"],
        "uncontrolled_source_routes": incomplete_route_manifest["investigation_assurance"]["uncontrolled_source_routes"],
        "adverse_candidate_reviews": incomplete_route_manifest["investigation_assurance"]["adverse_candidate_reviews"],
    }
    incomplete_route_manifest["investigation_assurance"]["review_records_hash"] = sha256_obj(records_payload)
    assert evaluate_manifest(incomplete_route_manifest)["status"] == STATUS_INVESTIGATION_INCOMPLETE
    structure_tampered_manifest = copy.deepcopy(manifest)
    structure_tampered_manifest["investigation_assurance"]["obligations"][2]["source_ids"] = ["S_DEEP_RESEARCH"]
    records_payload = {
        "obligations": structure_tampered_manifest["investigation_assurance"]["obligations"],
        "source_dispositions": structure_tampered_manifest["investigation_assurance"]["source_dispositions"],
        "uncontrolled_source_routes": structure_tampered_manifest["investigation_assurance"]["uncontrolled_source_routes"],
        "adverse_candidate_reviews": structure_tampered_manifest["investigation_assurance"]["adverse_candidate_reviews"],
    }
    structure_tampered_manifest["investigation_assurance"]["review_records_hash"] = sha256_obj(records_payload)
    assert evaluate_manifest(structure_tampered_manifest)["status"] == STATUS_INVESTIGATION_INCOMPLETE
    tests += 1

    unresolved_material_manifest = copy.deepcopy(manifest)
    unresolved_material_manifest["investigation_assurance"]["adverse_candidate_reviews"][4]["unresolved"] = True
    records_payload = {
        "obligations": unresolved_material_manifest["investigation_assurance"]["obligations"],
        "source_dispositions": unresolved_material_manifest["investigation_assurance"]["source_dispositions"],
        "uncontrolled_source_routes": unresolved_material_manifest["investigation_assurance"]["uncontrolled_source_routes"],
        "adverse_candidate_reviews": unresolved_material_manifest["investigation_assurance"]["adverse_candidate_reviews"],
    }
    unresolved_material_manifest["investigation_assurance"]["review_records_hash"] = sha256_obj(records_payload)
    assert evaluate_manifest(unresolved_material_manifest)["status"] == STATUS_INVESTIGATION_INCOMPLETE
    tests += 1

    material_refutation_manifest = copy.deepcopy(manifest)
    material_refutation_manifest["investigation_assurance"]["adverse_candidate_reviews"][5]["materiality"] = "MATERIAL"
    material_refutation_manifest["investigation_assurance"]["adverse_candidate_reviews"][5]["attribution_status"] = "ENTITY_MATCH_CONFIRMED"
    material_refutation_manifest["investigation_assurance"]["adverse_candidate_reviews"][5]["disposition"] = "ADMITTED_MATERIAL_CORE_REFUTATION"
    material_refutation_manifest["investigation_assurance"]["adverse_candidate_reviews"][5]["material_core_refutation"] = True
    records_payload = {
        "obligations": material_refutation_manifest["investigation_assurance"]["obligations"],
        "source_dispositions": material_refutation_manifest["investigation_assurance"]["source_dispositions"],
        "uncontrolled_source_routes": material_refutation_manifest["investigation_assurance"]["uncontrolled_source_routes"],
        "adverse_candidate_reviews": material_refutation_manifest["investigation_assurance"]["adverse_candidate_reviews"],
    }
    material_refutation_manifest["investigation_assurance"]["review_records_hash"] = sha256_obj(records_payload)
    assert evaluate_manifest(material_refutation_manifest)["status"] == STATUS_MATERIAL_COUNTEREVIDENCE_CONFIRMED
    tests += 1

    witness = derived["ai_assurance_witness"]
    assert witness["completed_milestones"] == 6
    assert witness["witness_outcome"] == "COMPLETED_PROACTIVE_NOVEL_DOMAIN_CO_CREATION_CHAIN"
    tests += 1

    core = derived["core_coarse"]
    assert core["family_count"] == len(MAPPING_PROFILES) * len(BASE_CORE_WEIGHTS) * 3 * len(REFERENCE_FRAMES)
    assert derived["core_frontier"]["status"] == "ROBUST_LOWER_BOUND_CERTIFIED"
    assert derived["core_frontier"]["declared_threshold_tests"]["55"] is True
    assert derived["core_frontier"]["declared_threshold_tests"]["68"] is True
    assert derived["core_frontier"]["declared_threshold_tests"]["70"] is True
    assert derived["core_frontier"]["declared_threshold_tests"]["75"] is False
    assert D(derived["core_frontier"]["guaranteed_lower_score"]) == D("70")
    tests += 1

    assert derived["label_invariance"] is True
    tests += 1

    chains = derived["philosophy_to_implementation_chains"]
    assert all(item["chain_outcome"] == "COMPLETE_PUBLIC_CLAIM_TO_IMPLEMENTATION_CHAIN" for item in chains.values())
    tests += 1

    hiroshima_frontier = derived["extended_individual_frontiers"]["K_HIROSHIMA_RESPONSIBLE_AI_EXECUTION"]
    assert D(hiroshima_frontier["threshold_frontier"]["guaranteed_lower_score"]) == D("70")
    tests += 1

    assert derived["future_milestones_not_scored"][0]["current_score_eligibility"] is False
    tests += 1

    deletion = derived["evidence_cluster_deletion"]
    assert set(deletion) == {f"DELETE_{cluster}" for cluster in OPTIONAL_CORE_CLUSTERS}
    tests += 1

    group_deletion = derived["evidence_group_deletion"]
    assert D(group_deletion["DELETE_ALL_AI_ASSURANCE_RELATED"]["guaranteed_lower_score"]) == D("67.75")
    assert D(group_deletion["DELETE_INTERSTOCK_CUSTOMER_OPERATING_MODEL"]["guaranteed_lower_score"]) == D("61")
    tests += 1

    prospective_hash = derived["prospective_charter"]["payload_hash"]
    assert is_sha256_hex(prospective_hash)
    assert prospective_hash == sha256_obj(prospective_charter_payload(manifest))
    tests += 1

    certificate = build_certificate()
    valid, replay_errors, replayed = semantic_replay_certificate(certificate)
    assert valid, replay_errors
    assert replayed is not None
    tests += 1

    tampered = copy.deepcopy(certificate)
    tampered["derived"]["core_coarse"]["status"] = "INDETERMINATE"
    # Do not reseal: the payload hash must catch direct tampering.
    valid, _, _ = semantic_replay_certificate(tampered)
    assert not valid
    tests += 1

    tampered_resealed = copy.deepcopy(certificate)
    tampered_resealed["inputs"]["mapping_profiles"][0]["dimension_weights"][0][1] = "0.99"
    tampered_resealed = seal_certificate({key: value for key, value in tampered_resealed.items() if key != "certificate_payload_hash"})
    valid, _, _ = semantic_replay_certificate(tampered_resealed)
    assert not valid

    gate_tampered = copy.deepcopy(certificate)
    gate_tampered["inputs"]["investigation_assurance"]["uncontrolled_source_routes"][0]["completed"] = False
    gate_tampered = seal_certificate({key: value for key, value in gate_tampered.items() if key != "certificate_payload_hash"})
    valid, _, _ = semantic_replay_certificate(gate_tampered)
    assert not valid
    tests += 1

    # The certificate does not depend on a separately distributed JSON artifact.
    assert certificate["security_boundary"]["semantic_replay_supported"] is True
    tests += 1

    return tests


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def read_json(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("evaluate", help="Print the compact evaluation summary")
    subparsers.add_parser("certificate", help="Emit the complete replayable certificate JSON to stdout")
    subparsers.add_parser("freeze", help="Emit the prospective charter payload and hash")
    verify_parser = subparsers.add_parser("verify", help="Verify and semantically replay a generated certificate")
    verify_parser.add_argument("certificate", help="Certificate JSON path, or '-' for stdin")
    subparsers.add_parser("self-test", help="Run deterministic built-in tests")
    subparsers.add_parser("summary-json", help="Emit a compact machine-readable summary")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command or "evaluate"

    if command == "evaluate":
        certificate = build_certificate()
        print_evaluation_summary(certificate)
        return 0
    if command == "certificate":
        print(json.dumps(canonicalize(build_certificate()), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if command == "summary-json":
        certificate = build_certificate()
        print(json.dumps(compact_summary(certificate["derived"]), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if command == "freeze":
        manifest = build_manifest()
        payload = prospective_charter_payload(manifest)
        print(json.dumps({"payload_hash": sha256_obj(payload), "payload": payload}, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if command == "verify":
        certificate = read_json(args.certificate)
        valid, errors, replayed = semantic_replay_certificate(certificate)
        print(f"valid: {valid}")
        if replayed is not None:
            replayed_core = replayed.get("core_coarse") or {}
            print(f"replayed_status: {replayed.get('status')}")
            print(f"replayed_core_status: {replayed_core.get('status')}")
            print(f"replayed_core_outcomes: {replayed_core.get('possible_outcomes')}")
        for error in errors:
            print(f"- {error}")
        return 0 if valid else 1
    if command == "self-test":
        count = run_self_tests()
        print(f"{count} self-tests passed")
        return 0
    parser.error(f"Unknown command: {command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
