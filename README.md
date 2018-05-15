Linear-transformed interaction time between
related processes
---

Information theory methods have become popular in reverse-engineering after Samoilov posted thesis in 
1997 and presented *Correlation Metric Construction (CMC)* and then *Entropy Metric Construction (EMC)* in 2001 [[1]](https://www.researchgate.net/publication/10732803_On_the_Deduction_of_Chemical_Reaction_Pathways_from_Measurements_of_Time_Series_of_Concentrations).

We assume mutual information as a good approach for estimating strength of interaction between two processes.
Methods based on the CMC or EMC often include one of the two most spreaded assumptions on delays.
On the one hand, delays are used to find maximum of mutual information by cropping one or both time series by the delay value, then mutual information is being calculated on cropped series. 
This way interaction delays assumed to be only *one-to-one* corresponded and the assumption is too restricted.
On the other hand, methods simply disregard the possibility of interaction being delayed or it's signification.

There we have an idea of measuring relations taking into account
possibility of interaction intervals to be linear-transformed.


Linear-transformed interaction time between related processes
---
Information theory methods have become popular in reverse-engineering after Samoilov posted thesis in 1997 and presented *Correlation Metric Construction (CMC)* and then *Entropy Metric Construction (EMC)*, as a generalization of *CMC* in 2001. [[1]](https://www.researchgate.net/publication/10732803_On_the_Deduction_of_Chemical_Reaction_Pathways_from_Measurements_of_Time_Series_of_Concentrations)

We assume mutual information as a good approach for estimating strength of interaction between two processes. Methods based on the *CMC* or *EMC* often include one of the two most spreaded assumptions on the delays. 

On the one hand, delays are used to find maximum of mutual information by cropping one or both time series by the delay value, then mutual information is being calculated on cropped series. The mutual information between two processes is then the maximum of mutual informations by all allowed delays. So it means that these cropped intervals are the place of interaction. This way delays supposed to be only “one-to-one” corresponded and the assumption is too restricted.

On the other hand, methods simply disregard the possibility of interaction being delayed, or it's signification at all.

There we have an idea of measuring relations taking into account possibility of interaction intervals to be linear-transformed.