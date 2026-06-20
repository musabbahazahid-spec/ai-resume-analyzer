from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_score(resume, job):

    emb = model.encode([resume, job])

    score = util.cos_sim(emb[0], emb[1])

    return float(score[0][0]) * 100