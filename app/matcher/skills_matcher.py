class SkillsMatcher:

    def match(self, resume_skills, jd_skills):

        resume = {s.lower() for s in resume_skills}
        job = {s.lower() for s in jd_skills}

        matched = sorted(list(resume & job))
        missing = sorted(list(job - resume))

        if len(job) == 0:
            score = 100.0
        else:
            score = round((len(matched) / len(job)) * 100, 2)

        return {
            "score": score,
            "matched": matched,
            "missing": missing
        }