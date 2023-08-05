########################################################################3456789
########################################################################72
import cStringIO  # For creating file-like strings
import examsage as es  # for writing math exams


#############################
# Define the Problem Set class
#############################
class Body(object):
    # Initialize
    def __init__(self, sections=[]):
        # Create a list of objects defined by the sections list from
        # the JSON configuration file
        self.sections = []
        for section in sections:
            self.add_section(section)

    def add_section(self, section):
        """Adds a question, new page, image, etc. to the assessment.

        This method will create an instance of the section object
        using the section_type key value in the JSON file."""

        # Identify the section type
        try:
            section_type = section.pop('section_type')
        except Exception as err:
            print(self.__class__)
            print(
                "Every item in the sections list of the config file must "
                "have a section_type attribute. Current problems list: " +
                str(self.sections))
            print(err)
            print('\n')

        # Constrction the object for the given section type
        # and append it to the problem set
        if section_type == 'Question':
            self.sections.append(es.section.Question(section))
        elif section_type == 'NewPage':
            self.sections.append(es.section.NewPage())
        elif section_type == 'InsertImage':
            self.sections.append(es.section.InsertImage(section))
        elif section_type == 'Ztable':
            self.sections.append(es.section.Ztable())
        else:
            raise Exception("Section type {} is not supported "
                            "by ExamSage".format(section_type))

    def write_tex(self, layout_path, versions):
        # Convert the list of sections to TeX and generate the parameter TeX
        # files for each problem

        # Create a file-like string buffer to hold the layout of the problems
        body_tex = cStringIO.StringIO()

        # Number of problems added to the assessment.
        problem_num = 0

        # Generate the problem layouts and the parameter files
        for i in range(len(self.sections)):
            # Determine whether the object is a Question
            if self.sections[i] is a es.sections.Question #hasattr(self.sections[i], 'write_layout'): #<------ DETERMINE OBJECT CLASS
                problem_num += 1
                # Create a question object using the defintion found at the
                # location identified by location[i]
                self.sections[i].write_layout(str(problem_num).zfill(2))

                # Write the layout of the problem
                # Identify the problem number
                body_tex.write("\t % Problem " +
                                 str(problem_num).zfill(2) + "\n")
                # Add the appropriate number of tab spaces to the beginning
                # of each line
                body_tex.write("\t\t".join(
                    self.sections[i].layout.splitlines(True)))
                body_tex.write("\n")

                # Generate parameters for each version of the assessment
                for version in versions:
                    self.sections[i].get_parameters(layout_path, version) #<-------- rewrite to store parameters in memory until the document is published?
            else:
                # Insert a page break or image or PDF
                body_tex.write("\t\t".join(
                    self.sections[i].layout.splitlines(True)))

        # Save the text in a string before closing the memory buffer
        self.tex = body_tex.getvalue()
        body_tex.close()
        # Replace the tab characters with 4 spaces
        self.tex.expandtabs(4)#<----- Magic number!!!
