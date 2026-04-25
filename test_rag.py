from services.rag_pipeline import RAGPipeline
#create object
rag=RAGPipeline()
rag.load_documents_from_texts(["Healthinsurance covers hospitalization expenses.","Life insurance provides financial support to family"])

print("RAG pipeline executed successfully")
