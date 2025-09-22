# AWS SDK GUI Manager

A simple graphical user interface for managing/interacting with AWS services, which was built with Python and PyQt6.

## Features

**EC2 Management**
- List all EC2 instances with status, type, and IP addresses
- Start, stop, and terminate instances

- Launch new instances (dialog interface) **Note**: dummy functionality used for demonstration, as mentioned in dependency notes for simplicity and load time reduction to the manager
- Real-time status updates

### 🪣 **S3 Management**
- Browse S3 buckets and objects
- Create and delete buckets
- Upload files with progress tracking
- Download files
- File size formatting and metadata display

### ⚡ **Lambda Management**
- List all Lambda functions with runtime and handler info
- Invoke functions with custom JSON payloads
- View function configuration and code information
- Real-time execution results and logs **Note**: Dummy logs functionality to reduce load and for simplicity. At present shows active concurrency being used by the function as well as how many invocations were done in the last 5 minutes using cloudwatch.

### 👤 **IAM Management**
- List IAM users and roles
- View creation dates and ARNs
- Expandable for policy management **Note**: This is dummied to reduce total load and keep simplicity for now

### 📚 **CloudFormation Management**
- List CloudFormation stacks with status
- View stack creation dates
- Expandable for stack operations **Note**: Other stack operations are dummied, since this would require large input and configuration going against simplicity from this GUI

### ⚙️ **Settings & Configuration**
- Configure AWS credentials securely
- Set default regions
- Test AWS connections
- Load existing AWS CLI configurations

## Technical Architecture

### **Multi-threaded Design**
- Background workers for all AWS API calls using QT thread workers
- UI with progress indicators
- Error handling and user feedback **Note**: Error and population is a bit off at times - WIP to improve

### **Modular Structure**
- Separate interface managers for each AWS service
- Reusable worker threads


### **Security Features**
- Password masking for secret keys
- Secure credential storage
- Connection testing before operations

## Installation & Setup


# Install dependencies
pip install -r requirements.txt

# Run the application
cd code_dependencies
python main.py

**Note**: The pip installation would most likely have to be done in a virtual env to avoid dependency clashes with Python that may arise 

## Key Programming Skills Demonstrated

### **GUI Development**
- PyQt6 widgets and layouts
- Event handling and signals/slots
- Custom dialogs and forms
- Progress bars and status updates

### **Concurrent Programming**
- QThread for background operations actively listens for inputs
- Signal/slot communication between threads

### **AWS SDK Integration**
- Boto3 client usage across multiple services
- Error handling for AWS API calls
- Credential management and configuration

### **Software Architecture**
- Modular design with clear separation for service managers
- Reusable components and patterns
- Extensible structure for new services - New service managers can be added as needed

### **User Experience**
- Simple Intuitive tabbed interface
- Real-time feedback and status updates
- Error handling with user-friendly messages
- Progress tracking for long operations(some of these progress bars are disabled just for speed and low load, but bottom bar will relay request and response info for the operation)

## Extensibility

The application is designed to be easily extended with additional AWS services:

1. Create new manager class 
2. Implement worker threads for API calls
3. Add tab to main application
4. Follow existing patterns/models for consistency


The above is just possible implementations that can extend the GUI manager but some of these may not be applicable in terms of the manager itself as performance may be an issue especially in face of numerous resources loaded per service/component. As you will see through the code and possibly testing it out, features are dummied out as mentioned above and through the logic to keep the core 