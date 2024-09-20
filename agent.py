from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = "gpt-4o-mini"

llm = ChatOpenAI(model=model, temperature=0.5)

template = \
"""Given the clinician provided urodynamic report, change it into a patient explainable and understandable report.

<rules>
- Grade 12 reading level
- Explanation of each line, including provided values and normal ranges for reference
- Provide a summary at the end of the report that consolidates all of the findings, focusing on explanations for potential symptoms
</rules>

<formatting>
- Overall report should be in markdown with appropriate headers. The biggest header should be no more than header 3
- Header 3: "Your Urodynamics Report"
- Introduction
- (body sections): explained UDS report per Rules
- Summary: each individual diagnosis explained, then explained in tandem and in connection with each other. Specifically pull in the data points that support each diagnosis.
</formatting>

Remember: always use the provided documentation to formulate your answer. Your language must be patient oriented at a grade 12 reading level.

Important note: if a report is not given, do not generate a report. Query the user to provide a report."""

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()