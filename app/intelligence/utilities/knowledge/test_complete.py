from app.intelligence.utilities.knowledge.enterprise_resume_pipeline import EnterpriseResumePipeline

def debug_enterprise_resume_pipeline():

    print("\n")
    print("=" * 100)
    print("ENTERPRISE PIPELINE FULL DEBUG")
    print("=" * 100)


    try:

        pipeline = EnterpriseResumePipeline()

        print("\n[PASS] Pipeline initialized")

        print(
            "Pipeline class:",
            type(pipeline)
        )


    except Exception as e:

        print("\n[FAIL] Pipeline initialization")

        print(
            type(e).__name__,
            e
        )

        raise


    # ---------------------------------------------------------
    # INPUT RESUME
    # ---------------------------------------------------------

    resume_text = """
    Muhammad Kashif

    Quality Assurance and Food Safety Professional

    15+ years experience in FMCG manufacturing,
    food safety systems, quality management,
    supply chain and business operations.

    Achievements:

    - Implemented FSSC 22000 food safety system
    - Achieved certification successfully
    - Increased production yield from 70% to 99%
    - Reduced customer complaints
    - Managed QA teams
    - Trained employees on hygiene practices

    Skills:

    HACCP
    BRCGS
    ISO 9001
    FSSC 22000
    Lean Six Sigma
    Python
    Data Analytics
    """


    print("\n")
    print("=" * 100)
    print("RUNNING PIPELINE")
    print("=" * 100)


    try:

        result = pipeline.process(
            resume_text
        )


        print("\n[PASS] Pipeline completed")


    except Exception as e:

        print("\n[FAIL] Pipeline execution")

        print(
            type(e).__name__,
            e
        )

        raise



    # =========================================================
    # STAGE INSPECTION
    # =========================================================


    print("\n")
    print("=" * 100)
    print("PIPELINE OBJECT ATTRIBUTES")
    print("=" * 100)


    print(
        dir(result)
    )



    # =========================================================
    # KNOWLEDGE DOCUMENT
    # =========================================================


    print("\n")
    print("=" * 100)
    print("KNOWLEDGE DOCUMENT")
    print("=" * 100)


    document = getattr(
        result,
        "knowledge_document",
        None
    )


    if document:

        print(
            "Document class:",
            type(document)
        )


        print(
            "\nDocument:"
        )


        print(
            document
        )


        print(
            "\nDocument fields:"
        )


        if hasattr(
            document,
            "__dict__"
        ):

            for key,value in document.__dict__.items():

                print(
                    f"{key}: {value}"
                )

    else:

        print(
            "NO KNOWLEDGE DOCUMENT FOUND"
        )



    # =========================================================
    # KNOWLEDGE GRAPH
    # =========================================================


    print("\n")
    print("=" * 100)
    print("KNOWLEDGE GRAPH")
    print("=" * 100)


    graph = getattr(
        result,
        "knowledge_graph",
        None
    )


    if graph:


        print(
            "Graph class:",
            type(graph)
        )


        nodes = graph.get_nodes()


        print(
            "Total Nodes:",
            len(nodes)
        )


        print("\nFIRST 10 NODES")

        for node in nodes[:10]:

            print(
                node
            )


    else:

        print(
            "NO GRAPH FOUND"
        )



    # =========================================================
    # KNOWLEDGE PROFILE
    # =========================================================


    print("\n")
    print("=" * 100)
    print("KNOWLEDGE PROFILE")
    print("=" * 100)


    profile = getattr(
        result,
        "knowledge_profile",
        None
    )


    if profile:


        print(
            "Profile class:",
            type(profile)
        )


        print("\nPROFILE DATA")


        for key,value in profile.__dict__.items():

            print(
                "\n----------------------------"
            )

            print(
                key
            )

            print(
                value
            )



    else:

        print(
            "NO KNOWLEDGE PROFILE FOUND"
        )



    # =========================================================
    # SUMMARY
    # =========================================================


    print("\n")
    print("=" * 100)
    print("SUMMARY PROFILE")
    print("=" * 100)


    summary = getattr(
        profile,
        "summary",
        None
    )


    if summary:

        print(
            type(summary)
        )


        for key,value in summary.__dict__.items():

            print(
                f"{key}: {value}"
            )



    # =========================================================
    # ACHIEVEMENTS
    # =========================================================


    print("\n")
    print("=" * 100)
    print("ACHIEVEMENT PROFILE")
    print("=" * 100)


    achievement = getattr(
        profile,
        "achievements",
        None
    )


    if achievement:

        for key,value in achievement.__dict__.items():

            print(
                f"{key}: {value}"
            )



    # =========================================================
    # LEADERSHIP
    # =========================================================


    print("\n")
    print("=" * 100)
    print("LEADERSHIP PROFILE")
    print("=" * 100)


    leadership = getattr(
        profile,
        "leadership",
        None
    )


    if leadership:

        for key,value in leadership.__dict__.items():

            print(
                f"{key}: {value}"
            )



    # =========================================================
    # SENIORITY
    # =========================================================


    print("\n")
    print("=" * 100)
    print("SENIORITY PROFILE")
    print("=" * 100)


    seniority = getattr(
        profile,
        "seniority",
        None
    )


    if seniority:

        for key,value in seniority.__dict__.items():

            print(
                f"{key}: {value}"
            )



    print("\n")
    print("=" * 100)
    print("DEBUG COMPLETED")
    print("=" * 100)



if __name__ == "__main__":

    debug_enterprise_resume_pipeline()