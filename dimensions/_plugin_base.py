"""DimensionPlugin ABC and shared dataclasses.

Every dimension under `dimensions/NN_name/plugin.py` subclasses
`DimensionPlugin` and implements `probe()`. `score()` has a sensible
default based on severity counts but can be overridden.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Any


SEVERITIES = ("critical", "major", "minor", "cosmetic")


@dataclass
class Finding:
    dimension: str
    severity: str  # one of SEVERITIES
    message: str
    evidence: str
    round: int = 1

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(
                "severity must be one of {}; got {!r}".format(SEVERITIES, self.severity)
            )


@dataclass
class DimensionResult:
    dimension: str
    score: float  # 0.0 - 1.0
    findings: List[Finding] = field(default_factory=list)
    passed: bool = True


class DimensionPlugin(ABC):
    """Base class for every audit dimension.

    Subclasses MUST set `name` and implement `probe()`. They MAY override
    `score()` and `regression_tests()`.
    """

    name: str = ""
    version: str = "0.1.0"
    runs_on: str = "skill"  # "skill" | "file" | "fleet"

    @abstractmethod
    def probe(self, target: Any) -> List[Finding]:
        """Run probes; return zero or more Finding objects."""
        raise NotImplementedError

    def score(self, findings: List[Finding]) -> float:
        """Default scoring: critical -> 0.0; -0.2 per major; -0.05 per minor."""
        if any(f.severity == "critical" for f in findings):
            return 0.0
        major = sum(1 for f in findings if f.severity == "major")
        minor = sum(1 for f in findings if f.severity == "minor")
        return max(0.0, 1.0 - (major * 0.2) - (minor * 0.05))

    def regression_tests(self) -> List[dict]:
        """Optional: regression tests to pin in the vault."""
        return []
