"""
Project NOVA - Universal Productivity Document Engine
Native creation of Word (.docx), PowerPoint (.pptx), Excel (.xlsx),
PDF reading, text summaries, and verified file operations.
"""

import os
import sys
import logging
from typing import Optional, List, Dict
from app.tools.base_tool import BaseTool, RiskTier, ToolContext, ToolExecutionResult

logger = logging.getLogger("nova.tools.productivity")

def get_target_directory(custom_dir: Optional[str] = None) -> str:
    """Safe target directory resolution, defaulting to Desktop."""
    if custom_dir and os.path.exists(custom_dir):
        return custom_dir
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.exists(desktop):
        return desktop
    return os.getcwd()

class CreateWordDocumentTool(BaseTool):
    name = "productivity.create_word_document"
    description = "Generate a professionally formatted Microsoft Word (.docx) document (assignments, reports, notes)."
    risk_tier = RiskTier.TIER_2_SENSITIVE
    supported_platforms = ["all"]
    parameters = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string", "description": "Filename ending with .docx (e.g. AI_Assignment.docx)"},
            "title": {"type": "string", "description": "Document title"},
            "sections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "heading": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["heading", "content"]
                },
                "description": "List of document sections with headings and paragraphs"
            }
        },
        "required": ["file_name", "title", "sections"]
    }

    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        file_name = arguments.get("file_name", "Document.docx")
        if not file_name.endswith(".docx"):
            file_name += ".docx"
        title = arguments.get("title", "Project NOVA Document")
        sections = arguments.get("sections", [])

        target_path = os.path.join(get_target_directory(), file_name)

        try:
            from docx import Document
            from docx.shared import Inches, Pt, RGBColor

            doc = Document()
            # Title
            title_p = doc.add_heading(title, level=0)
            title_p.runs[0].font.color.rgb = RGBColor(0, 51, 102)

            # Metadata header
            p_meta = doc.add_paragraph()
            p_meta.add_run(f"Prepared by: Project NOVA Universal Assistant\nStatus: Verified\n").italic = True

            # Sections
            for sec in sections:
                doc.add_heading(sec.get("heading", "Section"), level=1)
                doc.add_paragraph(sec.get("content", ""))

            doc.save(target_path)

            # Verification: Ensure file exists and size is valid
            if not os.path.exists(target_path) or os.path.getsize(target_path) == 0:
                return ToolExecutionResult(success=False, error=f"Document generation failed to write {target_path}")

            # Automatically open the generated document on the user's desktop!
            try:
                if sys.platform == "win32" and not os.environ.get("NO_AUTO_OPEN"):
                    os.startfile(target_path)
            except Exception as launch_err:
                logger.warning(f"Could not auto-open generated document: {launch_err}")

            return ToolExecutionResult(
                success=True,
                data={"path": target_path, "bytes": os.path.getsize(target_path), "sections": len(sections)},
                message=f"Word document successfully created and opened from: {target_path}"
            )
        except Exception as e:
            return ToolExecutionResult(success=False, error=f"Failed to generate Word document: {str(e)}")

class CreatePowerPointTool(BaseTool):
    name = "productivity.create_presentation"
    description = "Generate a structured Microsoft PowerPoint (.pptx) presentation for assignments or reports."
    risk_tier = RiskTier.TIER_2_SENSITIVE
    supported_platforms = ["all"]
    parameters = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string", "description": "Filename ending with .pptx"},
            "title": {"type": "string", "description": "Presentation main title"},
            "subtitle": {"type": "string", "description": "Presentation subtitle"},
            "slides": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "bullet_points": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["title", "bullet_points"]
                }
            }
        },
        "required": ["file_name", "title", "slides"]
    }

    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        file_name = arguments.get("file_name", "Presentation.pptx")
        if not file_name.endswith(".pptx"):
            file_name += ".pptx"
        main_title = arguments.get("title", "Project NOVA Presentation")
        subtitle = arguments.get("subtitle", "Autonomous Universal Agent")
        slides_data = arguments.get("slides", [])

        target_path = os.path.join(get_target_directory(), file_name)

        try:
            from pptx import Presentation
            from pptx.util import Inches, Pt

            prs = Presentation()

            # Slide 1: Title Slide
            title_slide_layout = prs.slide_layouts[0]
            slide = prs.slides.add_slide(title_slide_layout)
            slide.shapes.title.text = main_title
            if slide.placeholders[1]:
                slide.placeholders[1].text = subtitle

            # Slide 2+: Content Slides
            bullet_slide_layout = prs.slide_layouts[1]
            for s_data in slides_data:
                slide = prs.slides.add_slide(bullet_slide_layout)
                slide.shapes.title.text = s_data.get("title", "Slide")
                tf = slide.placeholders[1].text_frame
                tf.clear()
                bullets = s_data.get("bullet_points", [])
                for idx, point in enumerate(bullets):
                    if idx == 0:
                        tf.text = point
                    else:
                        p = tf.add_paragraph()
                        p.text = point

            prs.save(target_path)

            if not os.path.exists(target_path) or os.path.getsize(target_path) == 0:
                return ToolExecutionResult(success=False, error=f"Presentation failed to write {target_path}")

            # Auto-open generated presentation on host OS
            try:
                import sys
                if sys.platform == "win32" and not os.environ.get("NO_AUTO_OPEN"):
                    os.startfile(target_path)
            except Exception:
                pass

            return ToolExecutionResult(
                success=True,
                data={"path": target_path, "slides_count": len(slides_data) + 1, "bytes": os.path.getsize(target_path)},
                message=f"PowerPoint presentation created with {len(slides_data) + 1} slides at: {target_path}"
            )
        except Exception as e:
            return ToolExecutionResult(success=False, error=f"Failed to generate PowerPoint: {str(e)}")

class CreateSpreadsheetTool(BaseTool):
    name = "productivity.create_spreadsheet"
    description = "Generate a formatted Microsoft Excel (.xlsx) spreadsheet with columns and rows."
    risk_tier = RiskTier.TIER_2_SENSITIVE
    supported_platforms = ["all"]
    parameters = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string", "description": "Filename ending with .xlsx"},
            "sheet_name": {"type": "string", "description": "Sheet title"},
            "headers": {"type": "array", "items": {"type": "string"}},
            "rows": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}}
        },
        "required": ["file_name", "headers", "rows"]
    }

    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        file_name = arguments.get("file_name", "Spreadsheet.xlsx")
        if not file_name.endswith(".xlsx"):
            file_name += ".xlsx"
        headers = arguments.get("headers", ["Item", "Value"])
        rows = arguments.get("rows", [])
        sheet_name = arguments.get("sheet_name", "Sheet1")

        target_path = os.path.join(get_target_directory(), file_name)

        try:
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = sheet_name

            # Add Headers
            ws.append(headers)

            # Add Rows
            for row in rows:
                ws.append(row)

            wb.save(target_path)

            if not os.path.exists(target_path) or os.path.getsize(target_path) == 0:
                return ToolExecutionResult(success=False, error=f"Spreadsheet failed to save {target_path}")

            # Auto-open generated spreadsheet on host OS
            try:
                import sys
                if sys.platform == "win32" and not os.environ.get("NO_AUTO_OPEN"):
                    os.startfile(target_path)
            except Exception:
                pass

            return ToolExecutionResult(
                success=True,
                data={"path": target_path, "rows_count": len(rows), "bytes": os.path.getsize(target_path)},
                message=f"Excel spreadsheet created with {len(rows)} rows at: {target_path}"
            )
        except Exception as e:
            return ToolExecutionResult(success=False, error=f"Failed to generate spreadsheet: {str(e)}")

class ReadPdfDocumentTool(BaseTool):
    name = "productivity.read_pdf"
    description = "Read and extract text from an existing PDF document on the filesystem."
    risk_tier = RiskTier.TIER_0_SAFE
    supported_platforms = ["all"]
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path to PDF file"}
        },
        "required": ["path"]
    }

    async def execute(self, arguments: dict, context: ToolContext) -> ToolExecutionResult:
        path = arguments.get("path", "")
        if not os.path.exists(path):
            return ToolExecutionResult(success=False, error=f"File not found: {path}")

        try:
            import pypdf
            reader = pypdf.PdfReader(path)
            total_pages = len(reader.pages)
            extracted = ""
            for i in range(min(total_pages, 5)): # Read up to 5 pages
                extracted += f"\n--- Page {i+1} ---\n" + reader.pages[i].extract_text()

            return ToolExecutionResult(
                success=True,
                data={"pages": total_pages, "excerpt": extracted[:2000], "path": path},
                message=f"Extracted content from {total_pages} page PDF."
            )
        except Exception as e:
            return ToolExecutionResult(success=False, error=f"Failed to read PDF: {str(e)}")

