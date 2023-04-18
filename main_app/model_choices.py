STATUS = [
    ("AC", "Active"),
    ("IM", "Inactive - Matriculated"),
    ("IN", "Inactive - Non-Matriculated"),
    ("TA", "Transfer - Active"),
    ("TI", "Transfer - Inactive"),
    ("TU", "Transfer - Unknown Status"),
    ("AL", "Alumnae"),
    ("ME", "Memorial"),
    ("PI", "Permanent Inactivity"),
]

CHAPTER_STATUS = [
    ("AC", "Active"),
    ("IN", "Inactive"),
]

NICKNAME_STATUS = [
    ("RE", "Requested"),
    ("AP", "Approved"),
    ("QU", "Queued"),
    ("DE", "Denied"),
]

# Note that for this use case, the greek alphabet is missing Kappa.
GREEK_CLASS = [
    ("00", "Charter"),
    ("01", "Alpha"),
    ("02", "Beta"),
    ("03", "Gamma"),
    ("04", "Delta"),
    ("05", "Epsilon"),
    ("06", "Zeta"),
    ("07", "Eta"),
    ("08", "Theta"),
    ("09", "Iota"),
    (10, "Lambda"),
    (11, "Mu"),
    (12, "Nu"),
    (13, "Xi"),
    (14, "Omicron"),
    (15, "Pi"),
    (16, "Rho"),
    (17, "Sigma"),
    (18, "Tau"),
    (19, "Upsilon"),
    (20, "Phi"),
    (21, "Chi"),
    (22, "Psi"),
    (23, "Omega"),
]

for i in range(24, 47):
    GREEK_CLASS += ((i, f"Alpha {GREEK_CLASS[i-23][1]}"),)

for i in range(47, 70):
    GREEK_CLASS += ((i, f"Beta {GREEK_CLASS[i-46][1]}"),)


JOB_LEVEL = [
    ("00", "Internship"),
    ("01", "Entry"),
    ("02", "Associate"),
    ("03", "Analyst"),
    ("04", "Specialist"),
    ("05", "Manager"),
    ("06", "Senior Manager"),
    ("07", "Director"),
    ("08", "Senior Director"),
    ("09", "Executive"),
]

JOB_FAMILY = [
    ("FI", "Finance"),
    ("CS", "Community Service"),
    ("FU", "Fundraising"),
    ("SH", "Sisterhood"),
    ("IN", "Intake"),
    ("OP", "Operations"),
    ("ED", "Education"),
    ("RE", "Recruiting"),
    ("PR", "Public Relations"),
]

EVENT = [
    ("FU", "Fundraising"),
    ("SE", "Service"),
    ("PR", "Professional"),
    ("SI", "Sisterhood"),
    ("ED", "Educational"),
]
