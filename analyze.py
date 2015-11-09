import string
from collections import OrderedDict

header_title = 'Title'
header_experience = 'Experience'
header_skill = 'Skill'
title_multiplier = 0.15
skill_multiplier = 0.3
generic_multiplier = 0.1

def assign_key_multipler(job_description):
  key_multipler = {}
  header_keys = job_description.keys()

  for header in header_keys:
    if header == header_title:
      key_multipler.update({header: title_multiplier})
    elif header == header_skill:
      key_multipler.update({header: skill_multiplier})
    else:
      key_multipler.update({header: generic_multiplier})

  return key_multipler

def process_cv(extracted_resumes, key_multipler, job_description):
  result_list = []

  for resume in extracted_resumes:
    title_count, skill_count, generic_count = 0,0,0
    for multipler in key_multipler.keys():
      # Matching job title
      if resume.has_key(header_title) and multipler == header_title:

        # matching first level title
        if job_description[header_title] in resume[header_title]:
          title_count += key_multipler[multipler]

         # recurse in experience
        if resume.has_key(header_experience):
          for experience in resume[header_experience]:
            if experience.has_key(header_title):
              if job_description[header_title] in experience[header_title]:
                title_count += key_multipler[multipler]

      # Matching skills
      elif resume.has_key(header_skill)  and multipler == header_skill:
        for skill in resume[header_skill]:
          if skill in job_description[header_skill]:
            skill_count += key_multipler[multipler]

      elif resume.has_key(multipler):
        if job_description[multipler] in resume[multipler]:
          generic_count += key_multipler[multipler]

    score = title_count+skill_count+generic_count
    result_list.append({'Name': resume['Name'], 'Score': round(score, 2)})

  # Sort by score
  result_list = (sorted(result_list, key=lambda  t: t.get('Score', 0), reverse=True))
  return result_list

def process_analyzer(job_description, extracted_resumes):

  key_multipler = process_job_description(job_description)
  result_list = process_cv(extracted_resumes, key_multipler, job_description)



