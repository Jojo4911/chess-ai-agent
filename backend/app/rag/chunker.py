from pathlib import Path
import frontmatter
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- Configuration ---

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

DATA_DIR = Path(__file__).resolve().parent / "knowledge"

# --- Conversion fichier markdown -> Documents LangChain ---

def markdown_to_document(md_file: Path) -> Document:
    """
    Convertit un fichier markdown en objet Document LangChain

    Extrait l'en-tête YAML du fichier markdown pour créer les métadonnées (nom, eco, coups, source)
    Le texte qui suit l'en-tête est le texte principal
    """
    post = frontmatter.load(md_file)
    metadata = {
        "nom": post["nom"],
        "eco": post["eco"],
        "coups": post.get("coups", ""),
        "source": md_file.name,
    }

    return Document(page_content=post.content, metadata=metadata)

def path_to_documents(data_dir: Path = DATA_DIR) -> list[Document]:
    """Charge tous les .md de knowledge/ en liste de Documents LangChain."""
    return [markdown_to_document(f) for f in sorted(data_dir.glob("*.md"))]


# --- Chunking ---


def chunk_documents(
        documents: list[Document],
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Document]:
    """
    Découpe les documents en chunks avec RecursiveCharacterTextSplitter.
    Les métadonnées de chaque document sont propagées à tous ses chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", ", ", " ", ""],
    )

    return text_splitter.split_documents(documents)


# --- Point d'entrée ---


def main() -> None:
    """Exécute le pipeline de chunking"""
    chunks = chunk_documents(documents=path_to_documents())
    print(f"Nombre total de chunks : {len(chunks)}")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n === Chunk {i} ===")
        print(f"Contenu : {chunk.page_content[:80]}...")
        print(f"Métadonnées : {chunk.metadata}")

if __name__ == "__main__":
    main()