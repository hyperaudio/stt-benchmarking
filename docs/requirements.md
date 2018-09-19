No. | Requirement | Notes 
--- | ----------- | ----- 
R1 | Return WER | This tests for words only, compared to the reference transcript, using the formula in  https://en.wikipedia.org/wiki/Word_error_rate.  
R2 | Return punctuation accuracy. | Includes paragraph breaks (if included in the reference). 
R3 | Return capitalisation accuracy. 
R4 | Return timecode accuracy | What metric? For example average milliseconds difference from the reference?  
R5 | As little configuration as possible | Depend on test data format as much as possible for deciding which evaluation metrics to compute. 
R6 | Return processing time | How to measure? E.g., from receiving job ID to job complete API message.     
R7 | Return sentence error rate | Future requirement? 
R8 | Return total number of identified speakers 
R10 | Return correct speaker gender identification  | Should 'undetermined' count as an error? 
R11 | Language agnostic | Rely on user to provide tokenized input 
R12 | Include guidelines for the reference text file, eg normalisation. | Keep it minimal. Things like white spaces and curly apostrophes should be removed, but allow for house styles like EM dash/hyphen. 
R13 | For this release, support single channel audio.  | Come back to multichannel files in future release.  
R14 | Normalise confidence scores. | E.g. return all as %. Or normalise across providers by calculating average confidence score as function of WER.  
R15 | Return average confidence score for the transcript. 
R16 | Streams | Reminder for future thinking.  
R17 | Normalise reference transcript into internal extensible format  | E.g convert text, CTM and MLF into an internal format. The internal format is a list of tokens with metadata.
