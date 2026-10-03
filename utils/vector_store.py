import os

def init_vector_db():
    rates_db = [
        {"category": "Vitrified Tile Flooring", "rate": 80, "doc": "Vitrified Tile Flooring: ₹80 per sq. ft. including laying, skirting, and wastage material."},
        {"category": "Wall Plastering", "rate": 35, "doc": "Wall Plastering (Internal & External): ₹35 per sq. ft. using premium cement mortar mix."},
        {"category": "Painting", "rate": 25, "doc": "Emulsion Paint & Wall Finishing: ₹25 per sq. ft. including primer coats and wall putty."},
        {"category": "Structural", "rate": 450, "doc": "RCC Structure, Steel & Brickwork: ₹450 per sq. ft. built-up area rate baseline framework."},
        {"category": "Bathroom", "rate": 120, "doc": "Bathroom Ceramic Tiling & Sanitary Fitting: ₹120 per sq. ft. complete wet area package."},
        {"category": "Electrical", "rate": 55, "doc": "Electrical Wiring & Modular Switches: ₹55 per sq. ft. built-up area circuit distribution."},
        {"category": "Cement", "rate": 400, "doc": "Cement Requirement Benchmark: Approximately 0.4 bags of cement per sq. ft. of built-up area at standard market rates of ₹380-₹420 per bag."}
    ]
    return rates_db

def query_rates(query_text, n_results=3):
    rates_db = init_vector_db()
    query_lower = query_text.lower()
    
    matched_docs = []
    matched_metas = []
    
    for item in rates_db:
        if any(keyword in query_lower for keyword in item['category'].lower().split() or keyword in item['doc'].lower()):
            matched_docs.append(item['doc'])
            matched_metas.append({"category": item['category'], "rate": item['rate']})
            
    if not matched_docs:
        for item in rates_db[:n_results]:
            matched_docs.append(item['doc'])
            matched_metas.append({"category": item['category'], "rate": item['rate']})
            
    return matched_docs[:n_results], matched_metas[:n_results]