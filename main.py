num_papers = int(input())

papers_citations = []

i = 0

while i < num_papers:
    papers_citations.append(int(input()))
    i+=1
    
papers_citations.sort()

h_index = 0 

j = 0

limit_reached = False

while j < len(papers_citations) and not limit_reached:
    remaining_length = len(papers_citations) - (j)
    if (remaining_length) >= papers_citations[j]:
        h_index = papers_citations[j]
    elif (remaining_length) < papers_citations[j]:
        limit_reached = True
    j+=1

print(h_index)

