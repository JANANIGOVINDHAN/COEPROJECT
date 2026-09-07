import os
from io import BytesIO
from datetime import datetime
from sqlalchemy.orm import Session

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from backend.models.drift import DriftFinding, ScanRun
from backend.models.device import Device, Site

class ReportGeneratorService:
    @staticmethod
    def generate_pdf_report(db: Session, title: str = "Hospital Network Configuration Drift Sentinel - Executive Report") -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        story = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=15
        )
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=12,
            spaceAfter=8
        )
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#334155'),
            leading=12
        )

        # Title Section
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(f"Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} | Classification: Internal Hospital Security Audit", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=15))

        # Executive Summary Data
        total_devices = db.query(Device).count()
        total_sites = db.query(Site).count()
        total_findings = db.query(DriftFinding).count()
        unauthorized = db.query(DriftFinding).filter(DriftFinding.authorization_status != "Authorized").count()
        critical = db.query(DriftFinding).filter(DriftFinding.severity == "CRITICAL").count()
        high = db.query(DriftFinding).filter(DriftFinding.severity == "HIGH").count()

        summary_text = (
            f"This executive report details the continuous network configuration drift sentinel audit across "
            f"<b>{total_sites} hospital sites</b> and <b>{total_devices} active network infrastructure devices</b>. "
            f"A total of <b>{total_findings} drift findings</b> were detected during automated baseline comparison. "
            f"<b>{unauthorized} findings</b> are unapproved or unauthorized, including <b>{critical} Critical</b> and "
            f"<b>{high} High</b> risk severity items requiring immediate remediation."
        )
        story.append(Paragraph("1. Executive Summary", section_style))
        story.append(Paragraph(summary_text, body_style))
        story.append(Spacer(1, 12))

        # KPI Summary Table
        kpi_data = [
            ["Metric", "Count / Value", "Security Significance"],
            ["Total Sites Monitored", str(total_sites), "Distributed hospital campuses"],
            ["Total Infrastructure Devices", str(total_devices), "Core, Firewall, Switch, Wireless"],
            ["Total Drift Findings", str(total_findings), "Active configuration mismatches"],
            ["Unauthorized Changes", str(unauthorized), "No valid approved change ticket"],
            ["CRITICAL Risk Findings", str(critical), "Immediate security exposure"],
            ["HIGH Risk Findings", str(high), "Compliance or segmentation risk"]
        ]
        t = Table(kpi_data, colWidths=[150, 100, 250])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('ALIGN', (1,1), (1,-1), 'CENTER'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 15))

        # Critical Drift Findings Detail Table
        story.append(Paragraph("2. Critical & High Priority Drift Findings", section_style))
        findings = db.query(DriftFinding).filter(
            DriftFinding.severity.in_(["CRITICAL", "HIGH"])
        ).limit(15).all()

        if findings:
            f_table_data = [["Finding ID", "Site", "Device", "Field", "Severity", "Auth Status", "Risk"]]
            for f in findings:
                f_table_data.append([
                    f.finding_id[:12],
                    f.site_id,
                    f.hostname[:14],
                    f.field_name[:14],
                    f.severity,
                    f.authorization_status[:12],
                    f"{f.risk_score}/100"
                ])
            ft = Table(f_table_data, colWidths=[80, 60, 80, 80, 60, 80, 60])
            ft.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 7),
                ('ALIGN', (4,1), (-1,-1), 'CENTER'),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f1f5f9'), colors.white]),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('TOPPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(ft)
        else:
            story.append(Paragraph("No critical or high findings currently active.", body_style))

        story.append(Spacer(1, 15))
        story.append(Paragraph("3. Governance & Remediation Mandate", section_style))
        gov_text = (
            "All unauthorized drift findings must be investigated by Network Engineering and Security Operations. "
            "Remediation actions should be executed in accordance with hospital CAB change approval policies. "
            "Safe recommended remediation steps and CLI syntax are documented in the Sentinel Operations Console."
        )
        story.append(Paragraph(gov_text, body_style))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
