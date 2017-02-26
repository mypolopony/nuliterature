## Nuliterature

### Intro

In all reality, thre's nothing nü about this literature, except that it's new. 

The idea here is to make lexical (language?) models for different contemporary, most political commentators and media sources. There are lots of approaches, these are some that we're working on:

- Word2Vec is obviously played out, but the general ideas are decent enough to keep in mind
- N-gram frequency alone certainly isn't rich enough
- Kneser-Ney Smoothing seemed like an improvement on n-grams but now I'm not sure it's any more sophisticated
	https://en.wikipedia.org/wiki/Kneser%E2%80%93Ney_smoothing
- There is a set of academic 'fill-in-the-blank' models (which is basically the goal)
	https://pdfs.semanticscholar.org/7397/7371069fd2ba7e465a096cdf77a184ab2de5.pdf


### In General

I don't know enough about computational lingustics other than it seems to be a very natural bedfellow next to finite state models. But that's way above my pay grade. I do think, though, that it might be the explanation for why there is such an abundance of tools like CSLM, DALM, IRSTLM, Kylm, KenLM, LMSharp, MITLM, NPLM, OpenGrm, OxLM, RandLM, RNNLM, SRILM, VariKN, &c.

We'll train each source, based on jornalistic output for the past few years, to create these models.


### And Further

We would like to create a psychological profile of our authors and news sources. To see if our models have identified significant psychological traits, we can issue each profile a set of questions and ask how it might answer based on its particular style. 

There is no shortage of these kinds of personality tests, and they're generally distained, but I hope to try as much as the MMPI-2, at least, as well as some others. Unfortunately, these tests cost many dollars, so I cannot post the questions here in plain text, but I'll do my best to portray the assessment as accurately as possible while still adhering to licensing restrictions.

Having said that, if you're interested in digitizing neuropsych tests, do inquire within :)