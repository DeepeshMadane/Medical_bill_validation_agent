def search_tariff(retriever, service, hospital):
    service = normalize(service)
    hospital = normalize(hospital)

    results = retriever.invoke(service)

    for r in results:
        metadata = r.metadata

        db_service = normalize(metadata["service"])
        db_hospital = normalize(metadata["hospital"])

        # 🔥 flexible matching
        if service in db_service or db_service in service:
            if hospital in db_hospital:
                return r.page_content

    # fallback
    return results[0].page_content if results else None
def normalize(text):
    return text.lower().replace("&", "and").replace("  ", " ").strip()