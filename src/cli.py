"""Command-line interface for document gap analysis."""

import sys
import os
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import logging

from src.gap_analyzer import GapAnalyzer
from src.report_generator import ReportGenerator
from src.ai_provider import get_ai_provider

console = Console()


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Document Gap Analysis Tool - Compare documents to identify missing content."""
    pass


@cli.command()
@click.argument('user_document', type=click.Path(exists=True))
@click.argument('reference_documents', nargs=-1, type=click.Path(exists=True), required=True)
@click.option('--output', '-o', default='gap_analysis_report.md',
              help='Output file path for the report')
@click.option('--format', '-f', type=click.Choice(['markdown', 'html', 'json']),
              default='markdown', help='Report format')
@click.option('--provider', '-p', type=click.Choice(['openai', 'anthropic']),
              help='AI provider to use (overrides env variable)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def analyze(user_document, reference_documents, output, format, provider, verbose):
    """
    Perform gap analysis on a user document against reference documents.
    
    Example:
        gap-analyzer analyze user_doc.pdf ref1.pdf ref2.docx ref3.txt
    """
    setup_logging(verbose)
    
    if len(reference_documents) < 1:
        console.print("[red]Error: At least one reference document is required[/red]")
        sys.exit(1)
    
    console.print("\n[bold blue]Document Gap Analysis Tool[/bold blue]\n")
    
    # Display input files
    console.print(f"[green]User Document:[/green] {user_document}")
    console.print(f"[green]Reference Documents:[/green]")
    for i, ref_doc in enumerate(reference_documents, 1):
        console.print(f"  {i}. {ref_doc}")
    console.print()
    
    # Check for API keys
    try:
        if provider:
            os.environ['AI_PROVIDER'] = provider
        
        ai_provider = get_ai_provider()
        console.print(f"[green]✓[/green] Using AI provider: {ai_provider.__class__.__name__}\n")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        console.print("\n[yellow]Please set your API key in .env file or environment variables[/yellow]")
        sys.exit(1)
    
    # Perform analysis
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing documents...", total=None)
            
            analyzer = GapAnalyzer(ai_provider=ai_provider)
            report = analyzer.analyze(
                user_document,
                list(reference_documents)
            )
            
            progress.update(task, description="[green]✓[/green] Analysis complete")
        
        # Display summary
        console.print("\n[bold]Analysis Complete![/bold]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right")
        
        present = len([g for g in report.gaps if g.status == 'present'])
        partial = len([g for g in report.gaps if g.status == 'partial'])
        absent = len([g for g in report.gaps if g.status == 'absent'])
        total = len(report.gaps)
        
        table.add_row("Total Requirements", str(total))
        table.add_row("Present", f"[green]{present}[/green]")
        table.add_row("Partial", f"[yellow]{partial}[/yellow]")
        table.add_row("Absent", f"[red]{absent}[/red]")
        table.add_row("Coverage Score", f"[bold]{report.coverage_score:.1f}%[/bold]")
        
        console.print(table)
        console.print()
        
        # Generate report
        generator = ReportGenerator()
        generator.save_report(report, output, format=format)
        
        console.print(f"[green]✓[/green] Report saved to: [bold]{output}[/bold]")
        
        # Show warnings if needed
        if absent > 0:
            console.print(f"\n[yellow]⚠️  Warning:[/yellow] {absent} requirements are missing from the user document")
        
    except Exception as e:
        console.print(f"\n[red]Error during analysis:[/red] {e}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


@cli.command()
def check_setup():
    """Check if the environment is properly configured."""
    console.print("\n[bold blue]Checking Setup[/bold blue]\n")
    
    issues = []
    
    # Check for .env file
    if Path('.env').exists():
        console.print("[green]✓[/green] .env file found")
    else:
        console.print("[yellow]⚠[/yellow] .env file not found (optional)")
    
    # Check API keys
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if openai_key:
        console.print("[green]✓[/green] OpenAI API key configured")
    else:
        console.print("[yellow]⚠[/yellow] OpenAI API key not found")
        issues.append("Set OPENAI_API_KEY in .env file or environment")
    
    if anthropic_key:
        console.print("[green]✓[/green] Anthropic API key configured")
    else:
        console.print("[yellow]⚠[/yellow] Anthropic API key not found")
        issues.append("Set ANTHROPIC_API_KEY in .env file or environment")
    
    if not openai_key and not anthropic_key:
        console.print("\n[red]✗[/red] No AI provider API keys found")
        console.print("[yellow]At least one API key is required to use this tool[/yellow]")
    
    # Check AI provider setting
    provider = os.getenv('AI_PROVIDER', 'openai')
    console.print(f"[green]✓[/green] Default AI provider: {provider}")
    
    console.print()
    
    if issues:
        console.print("[yellow]Setup Issues:[/yellow]")
        for issue in issues:
            console.print(f"  - {issue}")
        console.print("\n[yellow]Copy .env.example to .env and add your API keys[/yellow]")
    else:
        console.print("[green]✓ Setup looks good![/green]")


@cli.command()
@click.argument('document_path', type=click.Path(exists=True))
def info(document_path):
    """Display information about a document."""
    from src.document_parser import DocumentParser
    
    console.print(f"\n[bold]Document Information[/bold]\n")
    
    try:
        parser = DocumentParser()
        doc = parser.parse(document_path)
        
        console.print(f"[cyan]File:[/cyan] {doc['file_name']}")
        console.print(f"[cyan]Type:[/cyan] {doc['file_type']}")
        console.print(f"[cyan]Size:[/cyan] {doc['metadata'].get('file_size', 0):,} bytes")
        
        if 'page_count' in doc['metadata']:
            console.print(f"[cyan]Pages:[/cyan] {doc['metadata']['page_count']}")
        
        if 'paragraph_count' in doc['metadata']:
            console.print(f"[cyan]Paragraphs:[/cyan] {doc['metadata']['paragraph_count']}")
        
        content_length = len(doc['content'])
        word_count = len(doc['content'].split())
        
        console.print(f"[cyan]Characters:[/cyan] {content_length:,}")
        console.print(f"[cyan]Words:[/cyan] {word_count:,}")
        
        console.print(f"\n[dim]Preview (first 200 characters):[/dim]")
        console.print(doc['content'][:200] + "...")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == '__main__':
    cli()
