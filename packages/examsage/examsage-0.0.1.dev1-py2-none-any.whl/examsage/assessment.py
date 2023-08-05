########################################################################3456789
########################################################################72
import os  # for handling OS objects (for example files)
import errno  # for handling errors from OS objects
import subprocess  # for calling OS processes like LaTeX
import shutil  # for copying files
import cStringIO  # For creating file-like strings
import examsage as es  # for writing math exams


#############################
# Define the Assessment class
#############################
class Assessment(object):
    """Generate multiple versions of an assessment.

    This class contains the attributes specific to the assessment as
    defined in the assessment definition JSON file. Most of the work
    in generating the assessment PDFs is performed by this object.

    Parameters
    ----------
    course : obj of class `Course`
        Used internally for the header and file structure info
    assessment_json : dict
        Used to set the attributes of this assessment.
    num_of_versions : positive int
        Number of versions to create for each assessment

    Attributes
    ----------
    type_ : str
        Type of assessment (quiz, test, final exam, etc.).
        Will appear in the header.
    number : postive int
        Sequence of assessment type (Quiz 01, Quiz 02, etc.)
    period : str
        Range of dates during which the assessment can be
        administered. Will appear in the header.
    point_value : float
        Point value of the assessment in the course. This point value
        will appear in the header of the instructor's key. To allow
        for bonus points, the sum total of the points assigned to the
        questions can be different than this point value.
    sections : list of dict
        Used to set the attributes of each section of the assessment.

    Optional Attributes
    -------------------
    instructions : str
        The 'instructions' attribute can be used to include
        instructions, in TeX format, after the 'Printed Name' line.
    hints : str
        The 'hints' attribute can be used to include items like
        formulas or images, in TeX format, after the instructions
        but before the questions

    Methods
    -------
    write_layout
        Generates the Layout.tex file and the parameter files.
    publish_PDF
        Publishes PDFs of the assessment

    Futrure
    -------
    body : list of section objects <----------- In Progress 2/23
        Contains objects that will appear in the body of the
        assessment. Examples: question, new page, image, etc.
    add_section <--------- Future to replace the ProblemSet Class
        Adds a question, new page, image, etc. to the assessment.

        This method will create an instance of the section object
        using the section_type key value in the JSON file.
    max_points : property that returns an int
        Maximum number of points available in the assessment
    """

    # Initialize the assessment object
    def __init__(self, course, assessment_json, num_of_versions=1):
        self.course = course
        self.assessment_json = assessment_json
        self._num_of_versions = num_of_versions
        self.type_ = assessment_json['type_']
        self.number = assessment_json['number']
        self.period = assessment_json['period']
        self.point_value = assessment_json['point_value']
        self.sections = assessment_json['sections']

        ######################################
        ####### Optional assessment attributes
        # The 'instructions' attribute can be used to include instructions,
        # in TeX format, after the 'Printed Name' line.
        self.instructions = assessment_json.get('instructions', "")

        # The 'hints' attribute can be used to include items like
        # formulas or images, in TeX format, after the instructions
        # but before the questions
        self.hints = assessment_json.get('hints', "")

        ####### Optional assessment attributes
        ######################################

        # Create the body of this assessment
        self.body = es.Body(self.sections)

    @property
    def num_of_versions(self):
        return self._num_of_versions

    @num_of_versions.setter
    def num_of_versions(self, value):
        if value > 0 and isinstance(value, int):
            self._num_of_versions = value
        else:
            raise TypeError(
                'Assessment.num_of_versions must be a positive int'
            )

    @property
    def max_points(self)
        # Calculate the maximum amount of points possible on the assessment
        # This is necessary because
        # - instructors may want to include extra points in the assessment
        # - instructors may accidentally assign too many points to the
        #   problem set
        ######################
        #for i in range(len(self.problems)):
        #    # Confirm that the object is a problem with assigned points
        #    if hasattr(self.problems[i], 'points'):
        #        self.max_points += sum(self.problems[i].points)
        max_points = 0 #<------ Not implemented 20190227
        return max_points

    # Set properties used for creating the file structure
    @property
    def _ordinal_number(self, length=2):
        # The assessment number folders should be named with
        # leading zeros to maintain alphanumeric order
        return str(self.number).zfill(length)

    @property
    def _versions(self):
        # The version folders should be named with
        # leading zeros to maintain alphanumeric order
        versions = []
        leadingZeros = len(str(self.num_of_versions))
        for i in range(1, self.num_of_versions + 1):
            versions.append(str(i).zfill(leadingZeros))
        return versions

    @property
    def _path(self):
        # Location to save the assessment TeX and parameter files
        # These files can be manually edit at a later date to create
        # a new version of the assessment or fix minor errors.
        return os.path.join(
            self.course._path,
            self.type_,
            self._ordinal_number,
        )

    def write_layout(self):
        """Generate the Layout.tex file and the parameter files.

        The Layout.tex file contains information that is the same for
        all versions of the assessment: the list of problems,
        point values, etc. The parameter files contain information that
        changes between versions (same questions different numbers).

        """

        # Create the directory for parameter files if necessary
        path = self._path
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # Write the body TeX for the problem set
        self.body.write_tex(path, self._versions)

        # Populate the Layout.tex with the list of problems and save
        # it to self._path.
        layoutTeX = r"""\def \parametersLocation{{"{parametersLocation_}"}}

\def \Examclass {{
    {{{courseName_}}} \\~\\
    {{\small {courseFormat_}}}
    }}

\def \Examname {{
    {assessmentType_} {assessmentNumber_}.\version{{}} - {ofPoints_} Points
    \\~\\ {{\small Assessing Period: {period_}}}
    }}

\def \Maxpoints {{{maxPoints_} points}}

\def \Notice{{
    {{\footnotesize
        \textbf{{FOR INSTRUCTORS ONLY \\
        (Max. of \Maxpoints)}}
    }}
}}

\ExamNameLine

{instructions_}

{hints_}

\begin{{enumerate}}
{problems_layout_}
\end{{enumerate}}
""".format(parametersLocation_=r'\version/',
           courseName_=self.course.name,
           courseFormat_=self.course.schedule_type,
           assessmentType_=self.type_,
           assessmentNumber_=self._ordinal_number,
           ofPoints_=self.point_value,
           maxPoints_=self.max_points,
           period_=self.period,
           instructions_=self.instructions,
           hints_=self.hints,
           problems_layout_=self.body.tex  # <-------------- Replace 20190227
          )

        # Save the Layout.tex to self._path
        self._string_to_file(layoutTeX, path, 'Layout.tex')

    def publish_PDF(self, publish_keys):
        """Publish PDFs of the assessment to self.course._path/PDF/

        Parameters
        ----------
        publish_keys : bool
            When `True`, generates the assessment keys and assessments
            When `False, only generates the assessments

        """

        # Parameters passed to the write_main_tex method
        # TeX bools are spelled with all lower case letters
        if publish_keys:
            keys = ['false', 'true']
        else:
            keys = ['false']

        for version in self._versions:
            for key in keys:
                # Name the assessment
                basename = '{schedule} - {type} {number} - {version}'.format(
                    schedule=self.course.schedule_type,
                    type=self.type_,
                    number=self._ordinal_number,
                    version=version,
                )
                if publish_keys:
                    basename = basename + ' - KEY'

                self._write_main_tex(version, key, basename + '.tex')

                # Run LaTeX
                print('Publishing: ' + basename)
                subprocess.call(
                    [
                        'xelatex',
                        '-interaction=batchmode',
                        '-jobname=' + basename,
                        basename + '.tex'
                    ],
                    cwd=self._path
                )
                # Run Sage
                subprocess.call(
                    [
                        'sage',
                        basename + '.sagetex.sage'
                    ],
                    cwd=self._path
                )

                # Run LaTeX again

                # Unknown errors occur when using Latexmk. The errors appear
                # to be related to the names of the automatically
                # generated files
                subprocess.call(
                    ['latexmk',
                     '-pdf',
                     '-f',
                     '-g',
                     '-silent',
                     '-interaction=batchmode',
                     '-jobname=' + basename,
                     basename + '.tex'
                    ],
                    cwd=self._path
                )

                # Copy the PDF to PDFdir
                source = os.path.join(self._path, basename + '.pdf')
                dest = os.path.join(self.course._PDFdir, basename + '.pdf')
                print('Published!')

                shutil.copyfile(source, dest)

    def _write_main_tex(self, version, key='false', basename='main.tex'):
        # Support fuction for publish_PDF. Writes the main.tex file.
        # This file defines the basic properties of the PDF
        # (font, margins, ...), then calls the Layout.tex file.

        mainTeX = r"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%% Purpose %%%%%%%%%%%%%%%%%%%%

%   main.tex is the first file the compiler reads. Use this file to:
%   - turn the answer key on or off via the toggle 'keyforInstr'
%   - set the semester and year
%   - select the assessment and version to be generated

%%%%%%%%%%%%%%%%%%%%self._pathpose %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The fleqn option aligns all equations on the left
\documentclass[12pt,fleqn]{{article}}

\usepackage{{preamble}}

% This flag determines whether the instructor key will be provided
\newtoggle{{keyforInstr}}
\toggle{instructor_key_}{{keyforInstr}}

% This flag determines whether the student answer key will be provided
\newtoggle{{key}}
\toggle{student_key_}{{key}}

% If displaying the instructor's key, make sure that the student's
% key is visible too.
\iftoggle{{keyforInstr}}{{
    \toggletrue{{key}}
}}{{% else
}}

\MakeHeaderFooter

\begin{{document}}

\def \Examterm {{{term_}}}
\def \questionDir {{"{question_dir_}"}}

% Choose the assessment to create

\def \version{{{version_}}}    \import{{"{layout_path_}"}}{{Layout.tex}}

\end{{document}}

        """.format(
            instructor_key_=key,
            student_key_=key,
            term_=self.course.term,
            version_=version,
            layout_path_='',
            question_dir_=self.course.question_dir)
        # Save the main.tex to self._path
        print('------------->' + str(self._path))
        print('------------->' + str(basename))
        self._string_to_file(mainTeX, self._path, basename)

    def _string_to_file(self, string, path, name):
        # Writes a string to a file at /path/name

        # Create the directory if necessary
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # Write the file.
        filename = os.path.join(path, name)
        with open(filename, 'w') as f:
            f.write(string)

    def __repr__(self):
        return (r"Assessment(course={course}, "
                "assessment_json={assessment_json}, "
                "num_of_versions={num_of_versions})".format(
                    course=self.course,
                    assessment_json=self.assessment_json,
                    num_of_versions=self.num_of_versions,
                ))


########################################################################3456789
########################################################################72
