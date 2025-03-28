import re

class Clean:
    @staticmethod
    def full_clean(prereq_string: str) -> str:
        if prereq_string:
            return Clean.remove_prereq(Clean.remove_coreq(Clean.remove_antireq(prereq_string)))
        return ""
    
    def remove_antireq(prereq_string: str) -> str:
        if prereq_string:
            return re.sub(r"Antireq:.*|Antirequisite:.*", "", prereq_string).strip()
        return ""

    def remove_coreq(prereq_string: str) -> str:
        if prereq_string:
            return re.sub(r"Coreq:.*|Corequisite:.*", "", prereq_string).strip()
        return ""
    
    def remove_prereq(prereq_string: str) -> str:
        if prereq_string:
            return re.sub(r"Prereq: |Prerequisite: ", "", prereq_string).strip()
        return ""