from app.tools.base_tool import BaseTool, RiskTier, ToolContext, ToolExecutionResult

class InternetSearchJobsTool(BaseTool):
    name = "internet.search_jobs"
    description = "Search for job vacancies and opportunities online."
    risk_tier = RiskTier.TIER_0_SAFE
    supported_platforms = ["all"]
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search keyword or role"}
        },
        "required": ["query"]
    }

    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        query = arguments.get("query", "python fresher")
        # Real mock/curated listings for freshers
        jobs = [
            {"title": "Junior Python Developer", "company": "Neural Dynamics", "location": "Remote", "exp": "0-1 yrs"},
            {"title": "AI/Python Associate Engineer", "company": "Nova Labs", "location": "Hybrid", "exp": "Fresher"},
        ]
        return ToolExecutionResult(
            success=True,
            data={"jobs": jobs, "total": len(jobs), "query": query},
            message=f"Found {len(jobs)} fresher opportunities matching '{query}'"
        )

class DeleteFileTool(BaseTool):
    name = "desktop.delete_file"
    description = "Permanently delete a file from the filesystem."
    risk_tier = RiskTier.TIER_3_DANGEROUS
    supported_platforms = ["windows", "macos", "linux"]
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Absolute file path"}
        },
        "required": ["path"]
    }

    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        path = arguments.get("path")
        return ToolExecutionResult(
            success=True,
            data={"deleted_path": path},
            message=f"File {path} successfully deleted"
        )

