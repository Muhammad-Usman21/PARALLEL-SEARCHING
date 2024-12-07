from fpdf import FPDF

def create_research_papers(papers):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 10)
            self.cell(0, 10, self.title, 0, 1, 'C')

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    # For each paper, generate a PDF with expanded sections
    for idx, paper in enumerate(papers):
        # Updated Code Using multi_cell
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.title = paper['title']
        pdf.add_page()

        # Title
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 18)
        pdf.multi_cell(0, 8, paper['title'], align='C')  # Using multi_cell for title
        pdf.ln(5)

        # Author
        pdf.set_font('Arial', 'I', 15)
        pdf.multi_cell(0, 8, f"Author: {paper['author']}")  # Using multi_cell for author
        pdf.ln(8)

        # Abstract Section
        pdf.set_font('Arial', 'B', 14)
        pdf.multi_cell(0, 8, "Abstract:")  # Section heading
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, paper['abstract'])  # Abstract content
        pdf.ln(10)

        # Introduction Section
        pdf.set_font('Arial', 'B', 14)
        pdf.multi_cell(0, 8, "Introduction:")  # Section heading
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 6, paper['content'])  # Introduction content
        pdf.ln(10)

        # Methodology Section
        if 'methodology' in paper:
            pdf.set_font('Arial', 'B', 14)
            pdf.multi_cell(0, 8, "Methodology:")  # Section heading
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(0, 6, paper['methodology'])  # Methodology content
            pdf.ln(10)

        # Results Section
        if 'results' in paper:
            pdf.set_font('Arial', 'B', 14)
            pdf.multi_cell(0, 8, "Results:")  # Section heading
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(0, 6, paper['results'])  # Results content
            pdf.ln(10)

        # Conclusions Section
        if 'conclusions' in paper:
            pdf.set_font('Arial', 'B', 14)
            pdf.multi_cell(0, 8, "Conclusions:")  # Section heading
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(0, 6, paper['conclusions'])  # Conclusions content
            pdf.ln(10)

        # References Section
        if 'references' in paper:
            pdf.set_font('Arial', 'B', 14)
            pdf.multi_cell(0, 8, "References:")  # Section heading
            pdf.set_font('Arial', '', 12)
            for ref in paper['references']:
                pdf.multi_cell(0, 6, f"- {ref}")  # Using multi_cell for references
            pdf.ln(10)

        
        # Save PDF
        filename = f"file{idx + 1}.pdf"
        pdf.output(filename)
        print(f"Created: {filename}")


papers = [
    {
        "title": f"Artificial Intelligence in Healthcare - Case Study {i}",
        "author": f"Dr. John Doe {i}",
        "abstract": (
            f"    Artificial intelligence (AI) has emerged as a transformative force across multiple disciplines, "
            f"including healthcare. This research paper {i} investigates the multifaceted applications of AI in healthcare, "
            f"highlighting its potential to revolutionize diagnostic processes, enhance treatment protocols, and improve "
            f"patient outcomes.\n\n     The study delves into various AI technologies, such as machine learning and natural language "
            f"processing, that enable healthcare professionals to analyze complex datasets, predict patient risks, and develop "
            f"personalized treatment plans. However, the paper also addresses significant challenges, including data privacy concerns, "
            f"regulatory hurdles, and the need for ethical AI practices. By exploring these aspects, the paper aims to provide a "
            f"comprehensive understanding of the role of AI in shaping the future of healthcare."
        ),
        "content": (
            f"    The content of this research paper {i} provides a thorough examination of the advancements in AI technologies and their "
            f"integration into healthcare systems. AI-driven diagnostic tools, such as image recognition algorithms, have demonstrated "
            f"unprecedented accuracy in detecting diseases like cancer and cardiovascular conditions. Similarly, predictive analytics "
            f"has enabled early detection of patient deterioration, allowing for timely interventions. The paper also discusses the role of "
            f"robotic process automation in administrative tasks, which streamlines operations and reduces costs. However, challenges such as "
            f"bias in AI models, lack of interoperability among systems, and resistance from healthcare professionals are analyzed in detail. "
            f"The discussion emphasizes the importance of collaboration between AI developers and medical experts to ensure the successful adoption "
            f"of these technologies in real-world settings.\n\n"
            f"    The content of this research paper {i} provides a thorough examination of the advancements in AI technologies and their "
            f"integration into healthcare systems. AI-driven diagnostic tools, such as image recognition algorithms, have demonstrated "
            f"unprecedented accuracy in detecting diseases like cancer and cardiovascular conditions. Similarly, predictive analytics "
            f"has enabled early detection of patient deterioration, allowing for timely interventions. The paper also discusses the role of "
            f"robotic process automation in administrative tasks, which streamlines operations and reduces costs. However, challenges such as "
            f"bias in AI models, lack of interoperability among systems, and resistance from healthcare professionals are analyzed in detail. "
        ),
        "methodology": (
            f"    This study adopts a mixed-methods approach, combining quantitative and qualitative research methods to assess the impact of AI in "
            f"healthcare. Data was collected from 15 hospitals over a period of five years, focusing on patient outcomes, diagnostic accuracy, and "
            f"treatment efficiency. Machine learning algorithms were applied to analyze over 500,000 patient records, identifying patterns and "
            f"predictive markers. Additionally, interviews with 50 healthcare professionals, including doctors, nurses, and IT specialists, were "
            f"conducted to gain insights into the practical challenges of implementing AI solutions. The study also includes a review of regulatory "
            f"frameworks governing AI in healthcare, ensuring a comprehensive understanding of its operational environment."
        ),
        "results": (
            f"    The findings of this research paper {i} are promising, showcasing the transformative potential of AI in healthcare. Hospitals that "
            f"integrated AI-driven diagnostic tools reported a 25% increase in accuracy for detecting complex conditions such as cancer and heart disease. "
            f"Additionally, the use of predictive analytics reduced patient readmissions by 18%, improving the overall efficiency of treatment protocols. "
            f"Administrative tasks, when automated using AI, saw a 40% reduction in time and cost, enabling healthcare workers to focus more on patient care. "
            f"However, the study also found that 30% of healthcare professionals expressed concerns about job displacement and the reliability of AI systems. "
            f"These findings underscore the need for balanced integration, combining human expertise with AI-driven insights."
        ),
        "conclusions": (
            f"    In conclusion, this research paper {i} highlights that AI is not just a technological advancement but a paradigm shift in the way healthcare "
            f"is delivered. While its potential to improve diagnostic accuracy, treatment efficiency, and administrative processes is undeniable, "
            f"significant efforts are required to address ethical, legal, and professional concerns. Training programs for healthcare professionals, "
            f"robust regulatory frameworks, and interdisciplinary collaboration are essential for the successful adoption of AI. Future research should "
            f"focus on developing explainable AI models and ensuring equitable access to AI-driven healthcare solutions, thus bridging the gap between "
            f"innovation and implementation."
        ),
        "references": [
            f"Smith, A. (2023). 'AI in Diagnostics: A New Era in Healthcare'. Journal of Medical AI, 15(3), pp. 45-60.",
            f"Brown, J. & Lee, K. (2022). 'Ethical Challenges in AI-Driven Healthcare'. Springer Publishing, pp. 120-145.",
            f"Johnson, P. (2021). 'Data Privacy and Security in AI Applications'. IEEE Transactions on Healthcare Informatics, 12(7), pp. 33-50."
        ]
    }
    for i in range(1, 51)
]

# Generate PDFs
create_research_papers(papers)
