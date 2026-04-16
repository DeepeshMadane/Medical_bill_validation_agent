from rag.vector_db import create_vector_db, get_retriever
from agent.langgraph_agent import build_graph

vector_db = create_vector_db("data/final_hospital_tariff_dataset.xlsx")
retriever = get_retriever(vector_db)

agent = build_graph(retriever)

result = agent({
    "image_path": "data/Dropped Image.png"
})

print(result["results"])