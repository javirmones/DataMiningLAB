#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def advicer_post_course(about, chapter, html, outlink, problem, sequential, static_tab, vertical, video, peergrading, discussion, dictation, n_access, n_problems, n_reproductions, group):
  if n_problems <= 10673.0:
    if problem <= 23.5:
      return "This course are doing well, keep the same way.\n"
    else:  # if problem > 23.5
      return "Probably the students, are being overwhelmed by all the knowledge, you should remove some problems.\n"
  else:  # if n_problems > 10673.0
    if html <= 15.5:
      if chapter <= 8.5:
        return "You shoul amplying your chapters and descondess a few the matter of the course, for a better transmission to your scholars.\n"
      else:  # if chapter > 8.5
        if sequential <= 61.0:
          if n_reproductions <= 26363.5:
            return "You have so low reproductions in total, should upgrade your visual content to make more usable course to the students.\n"
          else:  # if n_reproductions > 26363.5
            return "You are so transmisive, and dont need to make new audiovisual content.\n"
        else:  # if sequential > 61.0
          return "The sequential that you have in the course is good keep it!.\n"
    else:  # if html > 15.5
      if chapter <= 18.5:
        return "Maybe you should reduce your chapters, because your course are bordeline in quality!\n"
      else:  # if chapter > 18.5
        return "Definitive, you should condess your knowledge for a better transmission to your scholars.\n"

def predict_group_big_ml(sequential=None,video=None,n_reproductions=None):
    if (n_reproductions is None):
        return u'regular_course'
    if (n_reproductions > 4805):
        if (sequential is None):
            return u'regular_course'
        if (sequential > 76):
            if (video is None):
                return u'regular_course'
            if (video > 88):
                return u'regular_course'
            if (video <= 88):
                if (video > 74):
                    return u'quality_course'
                if (video <= 74):
                    return u'regular_course'
        if (sequential <= 76):
            if (n_reproductions > 12074):
                if (video is None):
                    return u'regular_course'
                if (video > 134):
                    return u'low_quality_course'
                if (video <= 134):
                    return u'regular_course'
            if (n_reproductions <= 12074):
                return u'low_quality_course'
    if (n_reproductions <= 4805):
        return u'low_quality_course'

if __name__ == '__main__':
    # TO DO hacer entrada de datos del curso