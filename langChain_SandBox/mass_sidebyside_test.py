from Query import get_Answer, get_BM25_Answer, rewrite_query, get_merged_answers_reWrite, get_merged_answers

questions = ["Who can use swords in this game?",
    "What does advantage and disadvantage mean?",
    "What are a character’s bonds, ideals, and flaws?",
    "What weapons is a wizard proficient with?",
    "How do you make a fighter character quickly?",
     "What happens when you roll a natural 1 on an attack roll?",
     "How does spellcasting work for clerics?",
     "What are the different types of actions in combat?",]

for question in questions:
    print("\n==============================\n")
    print(f"Original Question: {question}\n")
    print("---- Without Rewriting ----\n")
    get_merged_answers(question)
    print("\n---- With Rewriting ----\n")
    get_merged_answers_reWrite(question)