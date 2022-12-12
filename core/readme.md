# engine

## first naive version

* read line and process it 

## use classes and start optimizing (profiling)

* read packets and process those one after another

## introduce observer pattern 

* refactoring : separate computing from reporting : aims a proper integration with a GUI
* demonstrates the use of a long running thread bearing the analysis process

## TODO : introduce multi-threading 

* the main processing thread will only read in the file while threads will compute statistics chuck by chunk

## TODO : use a sqllite database and persist the processing

## TODO : support resume


