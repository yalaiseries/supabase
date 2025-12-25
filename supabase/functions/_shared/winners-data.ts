export const winnersData2025Csv = String.raw`"Topic","AI BIM Coordinator","SketchUp IFC AI-Classifier","LLMs Augmented Generative Design","Deffy AI – TOP Inspection"
"Representative Speaker","Samuel OOI (Lead)","Jason LI (Lead)","HUANG Ranzi (co-lead)","Ethan Ow (Rep) / YANG Fan (Lead)"
"Designation","BIM Associate, Kyoob Architects","Associate Director, DIST, M.Moser","Senior Engineer, Arup","Co-Founder, Wenti Labs"
"Linkedin","linkedin.com/in/samuelooi96","linkedin.com/in/leejayhom","linkedin.com/in/ranzi-huang","linkedin.com/in/ethanow"
"Profile Picture","","","", ""
"Lead","Samuel OOI (Lead)","Jason LI (Lead)","NA","YANG Fan (Lead)"
"Co-lead","Lucas LEE","NA","CHONG Wen Jin (co-lead)
HUANG Ranzi (co-lead)","NA"
"Team Members","NA","Mustafa TOFUR, M Moser Associates
Kim LAW, M Moser Associates
Jonathan LIM, OpenAI
Bryan CHEUNG, Cloudtim","Alex MAISSANT, Hendry OCTAVANUS, Wing CHAN","BAEY Yan Ling
CHEI Ji Hyo
Darius CHEN
Derrick WONG Kar Wai
Ethan OW
LOH Kah Miin"
"Slide","https://docs.google.com/presentation/d/1gp4G4688n4rvrudrXd4CaFIxWphfPUc2/edit?usp=drive_link&ouid=107799242509066406009&rtpof=true&sd=true","https://mmoser1-my.sharepoint.com/:f:/g/personal/jasonl_mmoser_com/En-D7yTjUPBPnSa2F4vxP9cBaa8YVd6V8yUdJx-AqagxIA?e=bcx0zN","https://drive.google.com/drive/folders/1BqH7Ht7k0Kd4I6ekaVG2rlGN3QZL8q2m?usp=sharing","https://docs.google.com/presentation/d/1O774dKfbHzhBF3jZmjZgcLiUmpnAkuDZnpkrmr8U4LA/edit?slide=id.p17#slide=id.p17"
"Other Links","NA","OneDrive folder password: sia","https://drive.google.com/drive/folders/1BqH7Ht7k0Kd4I6ekaVG2rlGN3QZL8q2m?usp=sharing","https://app.gitbook.com/o/SKy0EgI4M8SEyqUUwNIj/s/blgThU921eh4aZMvwcZS/"
"About","The AI BIM Coordinator addresses the rising complexity and responsibility in BIM coordination, especially under Singapore’s Corenet X mandate, which requires fully coordinated BIM models for design gateway submissions. Traditionally, BIM coordination relies on exporting models to Navisworks for clash detection, but this process generates thousands of unstructured clashes, many of which are false positives or minor modeling errors. This overwhelms coordinators, slows decision-making, and diverts focus from critical design issues like headroom constraints. The AI-driven solution leverages Google Gemini 2.0 for advanced clash analysis, using n8n for data processing and PyRevit for Revit integration. The AI filters out low-priority clashes, assigns actionable items to the right disciplines, and provides resolution instructions, significantly reducing manual effort. Testing showed substantial reductions in irrelevant clashes, faster processing, and improved accuracy in identifying high-impact issues. The result is accelerated feedback loops, cost savings, and more efficient design resolution. Future plans include developing platform-agnostic tools, enhancing AI model capabilities, and automating reporting to further streamline BIM workflows and compliance with industry standards.","The SketchUp AI Classifier tackles the problem of unstructured and poorly classified BIM components, which disrupt downstream workflows and reduce the credibility of digital coordination. Most SketchUp models, especially in large-scale interior projects, contain thousands of objects from various sources—many lacking proper IFC classification, metadata, or layer assignment. This disorganization leads to delays, errors, and significant manual cleanup.
The solution is a SketchUp plugin integrated with an agentic AI workflow: TensorFlow powers visual recognition, GPT-4o proposes initial classification and metadata assignment, GPT-o3-mini validates and reasons over the suggestions, and GPT-4o-mini formats and outputs clean, structured BIM data. The PoC achieved over 95% classification accuracy, with average processing times of 18 seconds per object, demonstrating high scalability and consistency.
This automation dramatically reduces manual workload, ensures models are ready for compliance and collaboration, and raises overall productivity. Next steps include enabling user-supplied API keys, developing a Revit-compatible version, and seeking industry partnerships for broader adoption.","This project investigates how Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) can enhance generative design workflows within the Rhino and Grasshopper environment. The core challenge lies in extracting rich geometric information from images, deploying LLM agents to interact with parametric scripts, and generating accurate GhPython code for complex design tasks. Current tools demand extensive human input, making the process labor-intensive and limiting creative exploration.

This proof of concept (PoC) explores the potential of LLMs to automate geometry extraction, code generation, and iterative design refinement—potentially leveraging RAG for improved accuracy.

Future development will focus on expanding input methods, refining system prompting, introducing specialized agents for geometry handling, and integrating with other platforms such as ETABS and Revit to broaden applicability and enhance generative design capabilities.

This work highlights the potential of AI to make computational design faster, more accessible, and more intuitive for designers and engineers.","Deffy addresses the inefficiencies and risks in manual site inspections and report generation in construction. Traditionally, site teams spend hours recording defects, cross-referencing codes, and compiling reports, leading to delays, errors, and commercial risks. Deffy is a Telegram-based AI chatbot powered by OpenAI GPT-4.1, enabling users to input unstructured data (images, text, voice) during site walks. The AI processes this data, cross-references regulatory codes using RAG, assesses defect severity, and generates standardized, high-quality inspection reports in minutes. Trials showed a 5X productivity boost, reducing report generation time from 150 to 30 minutes, with 80% accuracy in compliance checks. This automation frees up professionals for higher-value tasks, improves report quality and code compliance, and serves as a learning tool for junior staff. Planned enhancements include expanding compliance code coverage, integrating plan drawings for issue localization, and adding real-time rectification tracking and dashboards for comprehensive site management."
"Prize","1st","2nd","3rd","3rd"
"One sentence summary of What, Why, Benefits & How ","The AI BIM Coordinator streamlines BIM clash detection under Singapore’s Corenet X mandate by using AI to filter and prioritize issues, significantly reducing manual effort, improving accuracy, and accelerating design coordination through tools like Google Gemini 2.0, n8n, and PyRevit.","The SketchUp AI Classifier is a plugin that automates BIM component organization to solve the problem of unstructured models disrupting downstream workflows, delivering 95% classification accuracy and high-speed processing through an agentic AI pipeline powered by TensorFlow and GPT-based tools.","This PoC explores how LLMs and Retrieval-Augmented Generation (RAG) can streamline generative design in Rhino–Grasshopper by automating geometry extraction and GhPython code generation, addressing the manual bottlenecks that limit creativity, and using AI agents to enhance accuracy, accessibility, and integration with tools like ETABS and Revit.","Deffy is a Telegram-based AI chatbot that automates defect reporting and compliance checks on construction sites, addressing the inefficiencies of manual inspections by processing unstructured inputs through GPT-4.1 and RAG to generate accurate, standardized reports 5X faster, freeing professionals for higher-value tasks and enhancing site quality, compliance, and learning."
"Summary Slide","","","",""`;

export const winnersData2025InnovationCsv = String.raw`"Topic","ThinkSync AI Notes Processor","BIM 3D to 5D/6D Spec AI Agent","AI Contract Management"
"Representative Speaker","Frederico Ramos (Rep)","SEAH Kwee Yong (Rep)","CHAK Lee Meng (Rep)"
"Rep Designation","Principal, Aedas","Chartered Surveyor, SISV","Chief Executive Officer, CENS Private Limited"
"Linkedin","linkedin.com/in/frederico-ramos-architect","linkedin.com/in/kwee-yong-seah-160b3a21","linkedin.com/in/leemengchak"
"Profile Picture","","",""
"Lead","Frederico Ramos","SEAH Kwee Yong","CHAK Lee Meng"
"Co-lead","NA","CHENG Tai Fatt","TAN Tian Chong"
"Team Member","Brendan CHEONG, 
PHUAH Lin, 
YEOW Yann Herng","Gary ANG Chun Li, 
Jacky CHIN Kong Hin, 
LIM Wai Sing, 
Augustine YEE Meng Yew, 
Daniel CHOO","NA"
"Slide","https://docs.google.com/presentation/d/1D9qjrDjQNEAe8XJ7RfrJWyoTfDUoLjeMMFFQTLlTP2s/edit?usp=sharing","https://1drv.ms/p/c/330a1df49d0c90d3/EYB4ymT1td1Jg4Xzegk3Ae8BR2yCYbOJUeZwG7F8PuluyQ?e=cNvCbf","https://docs.google.com/presentation/d/1-pQyv5zqiUQPApOCS6u38PMoyzlDc5ZJ?rtpof=true&usp=drive_fs"
"Other Links","NA","NA","NA"
"About","This project addresses inefficiencies and miscommunication caused by fragmented project documentation, where critical updates, decisions, and files are scattered across emails, chats, and cloud storage, making it difficult for teams to stay aligned and act quickly. The core problem is the manual, time-consuming sorting and retrieval of relevant information from large volumes of unstructured emails and meeting notes, leading to delays, errors, and lost data. The solution leverages AI agents and automation tools (such as OpenAI GPT-4o and Microsoft Power Automate) to extract, classify, and structure emails and meeting notes within an integrated Microsoft 365 workflow. This enables teams to query important decisions while modeling, with parallel automated reviews of model areas in Revit against meeting minutes and guidelines. The system sends Teams notifications to highlight inconsistencies for user correction in real time. Outcomes include up to 70% time savings in manual sorting, improved accuracy, faster query responses, and streamlined documentation, enabling teams to focus on higher-value tasks while reducing miscommunication and operational risks.","The solution addresses the challenge of communicating and integrating data from designers’ BIM 3D models to downstream processes for quantity surveying and facilities management, which currently requires manual and error-prone workflows for generating specifications and maintenance checklists. This gap arises because existing tools struggle with seamless data exchange between BIM authoring software and downstream applications, leading to inefficiencies and delays in project documentation. The approach leverages AI agents like Google Vertex AI Gemini to query CSV data filtered from IFC model; uses generative AI to draft tailored specifications and checklists, and integrates historical templates and schedules of rates for improved accuracy and scalability. The outcomes include significant time savings, streamlined workflows, the ability to quickly generate accurate first drafts, and a scalable foundation for future project adoption.","This project introduces an AI-powered Construction Contract Management Solution (ACCMS) to address the inefficiencies and risks inherent in traditional contract management for construction projects. Current methods are plagued by manual processes, fragmented document handling, and a lack of real-time visibility, which cause delays, disputes, cost overruns, and compliance challenges—especially in multi-stakeholder environments with complex contract standards. The solution leverages generative AI (e.g., GPT-based models) for contract drafting and clause analysis, AI agents for real-time obligation monitoring, retrieval-augmented generation (RAG) for intelligent search and dispute resolution, and blockchain for automated milestone payments and audit trails—all integrated with project and site data via common BIM and project-management platforms. Key benefits include very substantial improvements in contract review time, very substantial reductions in legal disputes, enhanced compliance with international standards, greater project visibility, and streamlined automated payments—resulting in faster approvals, lower costs, and increased stakeholder trust."
"Prize","Innovation Award","Innovation Award","Innovation Award"
"One sentence summary of What, Why, Benefits & How ","This project uses AI agents and tools like GPT-4o and Power Automate to solve the inefficiencies of fragmented project documentation by automatically extracting, structuring, and querying unstructured emails and meeting notes, achieving up to 70% time savings, improving accuracy, and reducing miscommunication across teams.","This solution automates the conversion of BIM 3D data into specifications and maintenance checklists using Google Vertex AI Gemini, addressing manual inefficiencies by querying filtered IFC data and applying generative AI with historical templates, enabling faster, more accurate, and scalable documentation for QS and FM.","This project introduces an AI-powered contract management solution that integrates GPT-based drafting, AI agents, RAG search, and blockchain to streamline construction contracts, reducing delays, disputes, and costs while improving compliance, transparency, and payment automation across BIM-integrated workflows."
"Summary Slide","","",""`;

export const winnersData2024Csv = String.raw`"Topic","Automated Identification of Design Changes (Team 9)","Fire Code Checks (Team 3)","Carbon Now (Team 8)","Building Authorities Code Platform GPT (Team 6)","Architectural Ideation and Visualisation with Generative AI (Team 10)","Draco - Sketching/Collaging to AI Render tool (Team 5)","Automated and Intelligent generation of Massing Models and Visualisation from Design Brief (Team 7)"
"Category","Top Winners","Top Winners","Top Winners","Merit Prize","Merit Prize","Merit Prize","Merit Prize"
"Prize","First Prize Winner ($2500)","Second Prize Winner ($1500)","Third Prize Winner ($1000)","Merit Prize ($250)","Merit Prize ($250)","Merit Prize ($250)","Merit Prize ($250)"
"Lead","CHONG Shyh Hao (Lead)","Atenn Neoh (Lead)","Quentin SIM (Lead)","TAN Wei Sheng (Lead)","PONG Woon Wei (Lead)","Vignesh KAUSHIK (Lead)","Gerard TEO (Lead)"
"Co-lead","CHONG Wen Jin (co-Lead)","Bob Lee (co-Lead)","Darren TAN (co-Lead)","Anders Ang Wei Li (co-Lead)","Atenn NEOH (co-Lead)","Naomi Marcelle BACHTIAR (co-Lead)","Gyanish Kakati (co-Lead)"
"Team Members","Vincent PHOEN
Janis HO","Fujinami Yuji MALCOLM
Evangelina ONG
TANG Minjing
Yvonne ZHANG Jingyao","QUEK Li-En
Estelle MAK
David OKTAVIANUS
Ivonne SUWARNA
LIN Zhenyi","CHEK Hong Yao Gabriel
MAK Yiing Huey","LAU Siong Weng","CHEN Shujun
Karen LIEW","THET Naung Oo
LIM Kah Ying"
"Other Links","https://forms.gle/rPxSV5VVYPSbchya8","https://forms.gle/rPxSV5VVYPSbchya8","https://forms.gle/rPxSV5VVYPSbchya8","https://forms.gle/rPxSV5VVYPSbchya8","https://forms.gle/rPxSV5VVYPSbchya8","https://forms.gle/rPxSV5VVYPSbchya8","https://forms.gle/rPxSV5VVYPSbchya8"
"One sentence summary of What, Why, Benefits & How ","","","","","","",""`;

export const winnersExtraJson = String.raw`[
  {
    "year": 2024,
    "categories": [
      {
        "category": "Compliance",
        "useCases": [
          {
            "title": "CORENET X Compliance Checks (Team 2)",
            "team": "Submission (2024)",
            "award": "",
            "summary": "GenAI chatbot using RAG to generate a harmonised, up-to-date list of multi-agency regulations (e.g., URA/SCDF/LTA) for a given site early in concept design, reducing the manual 2–3 day process to minutes.",
            "links": []
          },
          {
            "title": "FSSD Requirement & Compliance Checks (Team 3)",
            "team": "Submission (2024)",
            "award": "",
            "summary": "Revit plugin proof-of-concept to automate compliant placement and checking of FSSD items (starting with fire extinguishers), aiming to reduce manual, error-prone compliance checks and recover design hours.",
            "links": [
              {
                "label": "GitHub",
                "url": "https://github.com/boblyx/fire"
              }
            ]
          },
          {
            "title": "Building Authorities Code Platform (Team 6)",
            "team": "Submission (2024)",
            "award": "",
            "summary": "RAG-based chat agent built with LlamaIndex to retrieve and summarise building code requirements from disparate sources, exploring indexing strategies, prompt engineering, and multi-agent approaches for large datasets.",
            "links": [
              {
                "label": "Reference",
                "url": "https://up.codes/"
              },
              {
                "label": "Reference",
                "url": "https://www.youtube.com/watch?v=TRjq7t2Ms5I&ab_channel=AIEngineer"
              }
            ]
          }
        ]
      },
      {
        "category": "Design Ideation + Generative Workflow",
        "useCases": [
          {
            "title": "Bubbles, no Troubles (Team 1)",
            "team": "Submission (2024)",
            "award": "",
            "summary": "Automates early space-planning exploration by generating parameterised bubble diagrams using agent-based simulation in Grasshopper (Kangaroo 2) and ChatGPT-assisted scripting, helping teams break the “first layout” mental block.",
            "links": [
              {
                "label": "Docs",
                "url": "https://drive.google.com/drive/folders/1a6TDwJO_DVy7VsbLaF9rD__K5WtRi9su?usp=sharing"
              }
            ]
          },
          {
            "title": "Layout Optimisation for Residential Feasibility Studies (Team 4)",
            "team": "Submission (2024)",
            "award": "",
            "summary": "ANN-based approach to predict parameters for efficient residential typical-floor layouts from brief inputs (area + unit mix), with a workflow spanning parametric modelling, optimisation (e.g., GA), and surrogate deep learning.",
            "links": [
              {
                "label": "Scripts/Models",
                "url": "https://drive.google.com/drive/folders/15iJIbrw9Tmc4XkcvHfMSAF57E6u4dfcB?usp=sharing"
              },
              {
                "label": "Training Files",
                "url": "https://drive.google.com/drive/folders/17h5owePT1gkZwSfjN-Y9nbbol-s8YIgG"
              },
              {
                "label": "Miro Board",
                "url": "https://miro.com/app/board/uXjVNrL36aQ=/"
              }
            ]
          },
          {
            "title": "Draco — Sketch/Collage to AI Render tool (Team 5)",
            "team": "Submission (2024)",
            "award": "Merit Prize ($250)",
            "summary": "Web-based sketching/collaging workflow (Excalidraw + React) that renders user intent via diffusion models and generates narrative text; explores a human-led ideation loop rather than prompt-only text-to-image.",
            "links": [
              {
                "label": "GitHub",
                "url": "https://github.com/vigneshkaushik/Project-Draco"
              }
            ]
          },
          {
            "title": "Automated Massing + Visualisation from Design Brief (Team 7)",
            "team": "Submission (2024)",
            "award": "Merit Prize ($250)",
            "summary": "Botpress/LLM extracts brief parameters + planning constraints into JSON and drives Rhino/Grasshopper massing generation with optioneering; optionally sends a prompt to Stable Diffusion to create quick style renders.",
            "links": [
              {
                "label": "Workflow",
                "url": "https://mediafiles.botpress.cloud/79b0c192-7acd-4d94-a90f-7a595a7fae6c/webchat/bot.html"
              }
            ]
          },
          {
            "title": "Architectural Design Quick Ideation & Visualisation with GenAI (Team 10)",
            "team": "Submission (2024)",
            "award": "Merit Prize ($250)",
            "summary": "Community learning guides and workflows for rapid design ideation/visualisation using Midjourney and locally-run Stable Diffusion (ControlNet/ComfyUI), including guidance on massing-to-GenAI for better spatial accuracy.",
            "links": [
              {
                "label": "Guide",
                "url": "https://docs.google.com/document/d/1bbSOV8KU564R3r7IMLo8D__DJjQ0j0xemPErpdhCG_I"
              },
              {
                "label": "Midjourney",
                "url": "https://www.midjourney.com/"
              },
              {
                "label": "PromeAI",
                "url": "https://www.promeai.pro/"
              }
            ]
          }
        ]
      },
      {
        "category": "Sustainability",
        "useCases": [
          {
            "title": "Quick / Full Cycle Carbon Calculator (Team 8)",
            "team": "Submission (2024)",
            "award": "Third Prize Winner ($1000)",
            "summary": "LLM-driven workflow to estimate embodied + operational carbon for existing buildings using public building data, ICE datasets and energy intensity assumptions, producing a rapid full-cycle footprint and offset guidance.",
            "links": []
          }
        ]
      },
      {
        "category": "Construction + Delivery",
        "useCases": [
          {
            "title": "Design Change Identification (Team 9)",
            "team": "Submission (2024)",
            "award": "First Prize Winner ($2500)",
            "summary": "Automated comparison of tender vs amended drawings to identify and label design changes, then generate descriptive text for variation documentation; targets large reductions in manual RVO review hours.",
            "links": [
              {
                "label": "Demo",
                "url": "https://object-detection-from-plan-drawings-2wv5vdvcfmezpgjxkixjbq.streamlit.app/YOLO_for_plans"
              },
              {
                "label": "Slides",
                "url": "https://docs.google.com/presentation/d/1NlYgJkV-Ma3LA47VO6c5FvEDeBX8Q-63/edit?usp=sharing"
              }
            ]
          }
        ]
      }
    ]
  }
]`;
