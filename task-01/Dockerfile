FROM python:3.13-slim@sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50 AS solver
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace
COPY environment/workspace/ /workspace/
COPY instruction.md /workspace/instruction.md
COPY LICENSE.bottle /LICENSE.bottle
CMD ["sh"]

# Author/evaluator image only. Never give this target to a solver.
FROM solver AS evaluator
WORKDIR /task-01
COPY environment/workspace/ ./environment/workspace/
COPY tests/ ./tests/
COPY solution/ ./solution/
COPY shortcuts/ ./shortcuts/
COPY verify.py ./verify.py
CMD ["python", "/task-01/verify.py", "all"]
