# LambdaBase

#### A library to support development of enterprise Serverless applications.

Serverless computing allows you to build and run applications without expending time and 
effort managing a server. Code is executed and billed only when called. Whilst this model 
provides many advantages such as horizontal scalability and reduced operational costs 
it creates it's own set of drawbacks such as debugging, testing and packaging.

There are numerous articles detailing the advantages and disadvantages of serverless 
architectures. It's worth considering all the salient points before starting down the 
serverless path however, in general, the zero configuration horizontal scalability 
and cost efficiencies are the most significant driving factors. The architecture 
described here helps to mitigate the disadvantages whilst magnifying the advantages.

As with any architecture there is no one size fits all solution, however, I've seen the 
following pattern implemented successfully in both Java and Python across multiple domains. 
I believe it provides a reasonable amount of flexibility whilst being sufficiently structured 
to help developers rapidly implement clean code. One of the guiding principles of this 
pattern is to overcome one of the most significant issues with Serverless - the difficulty 
of debugging and testing Serverless ready code in a local environment. 

The key design points and the basis for this architecture are as follows:

* Lambdas are grouped into functional areas. Each group contains multiple lambdas with 
different handlers for each function. This is to allow related lambdas to share common 
ode more easily and to simplify packaging and application structure.
* It should always be possible to execute and debug the lambda code locally.
* The configuration for each environment is packaged with each lambda. Which 
configuration file to use is specified by an environment variable which is specified 
at deployment time.
* The code to package and deploy each of the lambdas lives with the runtime code
* One click deployment to new environments should be trivial, and the concept of 
infrastructure as code should be maintained at all times.
* Dependency injection is used to allow alternative services to be injected into lambdas 
depending on where they are running.

The proposed architecture is designed to fulfill these high level goals whilst maintaining 
a flexibility which should allow future extension and resilience to changing project requirements.

Push to PyPi: 

python setup.py bdist_wheel
python -m twine upload lambdabase-0.x-py2-none-any.whl

