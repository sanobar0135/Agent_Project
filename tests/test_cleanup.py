from research.findings_cleanup import clean_papers

sample_papers = [
    {
        "title": "LoRA: Low-Rank Adaptation",
        "authors": ["Author A"],
        "year": 2021,
        "abstract": "  A   method   for fine tuning. ",
        "url": "https://example.com/1",
        "source": "arxiv"
    },
    {
        "title": "lora: low-rank adaptation",
        "authors": ["Author A"],
        "year": 2021,
        "abstract": "Duplicate paper",
        "url": "https://example.com/1",
        "source": "arxiv"
    },
    {
        "title": "QLoRA: Efficient Fine-Tuning",
        "authors": ["Author B"],
        "year": 2023,
        "abstract": "A new approach.",
        "url": "https://example.com/2",
        "source": "arxiv"
    }
]

result = clean_papers(sample_papers)

print("Papers before cleanup:", len(sample_papers))
print("Papers after cleanup:", len(result))

for paper in result:
    print(paper["title"])