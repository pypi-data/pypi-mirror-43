########################################################################3456789
########################################################################72
import cStringIO  # For creating file-like strings
import examsage as es  # for writing math exams


#############################
# Define the Problem Set class
#############################
class ProblemSet(object):
    # Initialize
    def __init__(self, sections):
        # Create a list of objects defined by the sections list from
        # the JSON configuration file
        self.problems = []
        for section in sections:
            # Identify the section type
            try:
                section_type = section.pop('section_type')
            except Exception as err:
                print(self.__class__)
                print(
                    "Every item in the sections list of the config file must "
                    "have a section_type attribute. Current problems list: " +
                    str(_problems))
                print(err)
                print('\n')

            # Constrction the object for the given section type
            # and append it to the problem set
            if section_type == 'Question':
                self.problems.append(es.section.Question(section))
            elif section_type == 'NewPage':
                self.problems.append(es.section.NewPage())
            elif section_type == 'InsertImage':
                self.problems.append(es.section.InsertImage(section))
            elif section_type == 'Ztable':
                self.problems.append(es.section.Ztable())
            else:
                raise Exception("Section type {} is not supported "
                                "by ExamSage".format(section_type))

        # Calculate the maximum amount of points possible on the assessment
        # This is necessary because
        # - instructors may want to include extra points in the assessment
        # - instructors may accidentally assign too many points to the
        #   problem set
        self.max_points = 0
        for i in range(len(self.problems)):
            # Confirm that the object is a problem with assigned points
            if hasattr(self.problems[i], 'points'):
                self.max_points += sum(self.problems[i].points)

    def write_layout(self, layout_path, versions):
        # Convert the list of problems to TeX and generate the parameter TeX
        # files for each problem

        # Create a file-like string buffer to hold the layout of the problems
        set_layout = cStringIO.StringIO()

        # Number of problems added to the assessment.
        problem_num = 0

        # Generate the problem layouts and the parameter files
        for i in range(len(self.problems)):
            # Determine whether the object is a Question
            if hasattr(self.problems[i], 'write_layout'):
                problem_num += 1
                # Create a question object using the defintion found at the
                # location identified by location[i]
                self.problems[i].write_layout(str(problem_num).zfill(2))

                # Write the layout of the problem
                # Identify the problem number
                set_layout.write("\t % Problem " +
                                 str(problem_num).zfill(2) + "\n")
                # Add the appropriate number of tab spaces to the beginning
                # of each line
                set_layout.write("\t\t".join(
                    self.problems[i].layout.splitlines(True)))
                set_layout.write("\n")

                # Generate parameters for each version of the assessment
                for version in versions:
                    self.problems[i].get_parameters(layout_path, version)
            else:
                # Insert a page break or image or PDF
                set_layout.write("\t\t".join(
                    self.problems[i].layout.splitlines(True)))

        # Save the text in a string before closing the memory buffer
        self.layout = set_layout.getvalue()
        set_layout.close()
        # Replace the tab characters with 4 spaces
        self.layout.expandtabs(4)
