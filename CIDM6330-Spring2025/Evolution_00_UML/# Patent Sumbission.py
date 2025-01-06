# Patent Sumbission

# File in-memory binary stream; this code is from stackoverflow question 26529269
import io

def splitPdf(file_):
    pdf = PdfFileReader(file)
    pages = []
    for i in range(pdf.getNumPages()):
        outputStream = io.BytesIO()

        output = PdfFileWriter()
        output.addPages(pdf.getPage(i))
        output.write(outputStream)

        # Move the stream position to the beginning,
        #making it easier for other code to read
        outputStream.seek(0)
        pages.append(outputStream)
    return pages


# Classes and methods to Submit a Patent

Class Filing():
    # Create Global call and Variables
    def __init__(self,filingNumber,apply):
        
        
    # Create filer Method
    def filer(self):
        self.filingNumber = nextFileNumber(new)
        self.paymentMethod = input("How are you paying? ")
        self.patentFolder = ()
        self.prototype = ()
        return filingNumber
        # Function to add next file
        def addFilingDocument()
            # this block of code should allow user to upload a pdf
            

        # Function to track interactions with patent design Reviewer
        def patentDesignerReview(conversation)
            conversation = ()
            question = ()
            answer = ()
            conversation = {question,answer}
            # this block of code should be able to track a conversation between Filer and Reviewer
    
    # Create inventor method
    def inventor(self):
        self.designNumber = input("What design number is this? ")
            #this block of code shold check that this inventor hasn't already used the design number
        self.desingDraftFile = {filename,filetype}

        # create createIdea function
        def createIdea ()
            # this block of code should allow user to input 
                # design name, discription, and any other features necessary
        
        # create createIdeaFile function
        def createIdeaFile ()
                #this block of code should allow inventor to edit and save a pdf
        
        # create createInventionDisclosure funciton
        def createInventionDisclosure ()
            #this should allow inventor to explain how the invention was created and reproduced
            
    # Create Registered Patent Practicioner Method
    def registeredPatentPracticioner(self)
        self.practicionerNumber
        self.meeting = {}

        def inventorMeeting()
            # code to note key topics in meeting and followup
        def logMeeting()
            # code to track meeting, date, start time, end time, notes
        def completeClientForm()
            # code to fill out a client form

    # Create weak entity method to start apply process and sumbit if complete
    def apply(self)
        self.filingNumber = filer()
        self.applicationNumber = application()
        self.provisionalFilingDate

        def saveProgress()
            #code to safe the unfinished application

        def submitApplication()
            #code to submit application to USPTO

    



#Application Class
Class Application():
    # Global Call and Variable
    #... to be continued... it's late and this is enough for first draft


