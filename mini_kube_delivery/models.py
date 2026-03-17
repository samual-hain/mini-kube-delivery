from dataclasses import dataclass
from enum import Enum
from typing import Optional


class JobStatus(Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


@dataclass
class Depot:
    id: str
    region: str
    capacity: int
    active_jobs: int = 0
    ready: bool = True


@dataclass
class Job:
    id: str
    region: str
    required_capacity: int = 1
    status: JobStatus = JobStatus.PENDING
    assigned_depot_id: Optional[str] = None


@dataclass
class DesiredState:
    region: str
    desired_routes: int
