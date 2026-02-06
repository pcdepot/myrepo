from __future__ import annotations

import uuid
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class EpubMetadata:
    title: str
    language: str
    identifier: str
    creator: str | None = None
    publisher: str | None = None
    date: str | None = None


def build_epub(output_path: Path, metadata: EpubMetadata, body: str, css: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w") as archive:
        archive.writestr(
            "mimetype",
            "application/epub+zip",
            compress_type=zipfile.ZIP_STORED,
        )
        archive.writestr(
            "META-INF/container.xml",
            _container_xml(),
            compress_type=zipfile.ZIP_DEFLATED,
        )
        archive.writestr(
            "OEBPS/styles.css",
            css,
            compress_type=zipfile.ZIP_DEFLATED,
        )
        archive.writestr(
            "OEBPS/chapter1.xhtml",
            _chapter_xhtml(metadata.title, metadata.language, body),
            compress_type=zipfile.ZIP_DEFLATED,
        )
        archive.writestr(
            "OEBPS/nav.xhtml",
            _nav_xhtml(metadata.title, metadata.language),
            compress_type=zipfile.ZIP_DEFLATED,
        )
        archive.writestr(
            "OEBPS/content.opf",
            _content_opf(metadata),
            compress_type=zipfile.ZIP_DEFLATED,
        )


def create_default_metadata(title: str, language: str) -> EpubMetadata:
    identifier = f"urn:uuid:{uuid.uuid4()}"
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return EpubMetadata(
        title=title,
        language=language,
        identifier=identifier,
        date=date,
    )


def _container_xml() -> str:
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">\n"
        "  <rootfiles>\n"
        "    <rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\"/>\n"
        "  </rootfiles>\n"
        "</container>\n"
    )


def _content_opf(metadata: EpubMetadata) -> str:
    creator = f"    <dc:creator>{metadata.creator}</dc:creator>\n" if metadata.creator else ""
    publisher = (
        f"    <dc:publisher>{metadata.publisher}</dc:publisher>\n"
        if metadata.publisher
        else ""
    )
    date = f"    <dc:date>{metadata.date}</dc:date>\n" if metadata.date else ""
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<package xmlns=\"http://www.idpf.org/2007/opf\" version=\"3.0\" unique-identifier=\"bookid\">\n"
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">\n"
        f"    <dc:title>{metadata.title}</dc:title>\n"
        f"    <dc:language>{metadata.language}</dc:language>\n"
        f"    <dc:identifier id=\"bookid\">{metadata.identifier}</dc:identifier>\n"
        f"{creator}{publisher}{date}"
        "    <meta property=\"dcterms:modified\">"
        + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        + "</meta>\n"
        "  </metadata>\n"
        "  <manifest>\n"
        "    <item id=\"nav\" href=\"nav.xhtml\" media-type=\"application/xhtml+xml\" properties=\"nav\"/>\n"
        "    <item id=\"chapter1\" href=\"chapter1.xhtml\" media-type=\"application/xhtml+xml\"/>\n"
        "    <item id=\"css\" href=\"styles.css\" media-type=\"text/css\"/>\n"
        "  </manifest>\n"
        "  <spine>\n"
        "    <itemref idref=\"chapter1\"/>\n"
        "  </spine>\n"
        "</package>\n"
    )


def _nav_xhtml(title: str, language: str) -> str:
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<!DOCTYPE html>\n"
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\""
        + language
        + "\">\n"
        "  <head>\n"
        f"    <title>{title}</title>\n"
        "    <meta charset=\"utf-8\"/>\n"
        "  </head>\n"
        "  <body>\n"
        "    <nav epub:type=\"toc\" id=\"toc\">\n"
        "      <h1>Contents</h1>\n"
        "      <ol>\n"
        "        <li><a href=\"chapter1.xhtml\">"
        + title
        + "</a></li>\n"
        "      </ol>\n"
        "    </nav>\n"
        "  </body>\n"
        "</html>\n"
    )


def _chapter_xhtml(title: str, language: str, body: str) -> str:
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<!DOCTYPE html>\n"
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\""
        + language
        + "\">\n"
        "  <head>\n"
        f"    <title>{title}</title>\n"
        "    <meta charset=\"utf-8\"/>\n"
        "    <link rel=\"stylesheet\" type=\"text/css\" href=\"styles.css\"/>\n"
        "  </head>\n"
        "  <body>\n"
        f"    <h1>{title}</h1>\n"
        f"    <p>{body}</p>\n"
        "  </body>\n"
        "</html>\n"
    )
