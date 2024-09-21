# Base image
FROM openjdk:17-jdk-alpine

# Work directory
WORKDIR /app

# Copy build artifact
COPY build/libs/my-survey-app-0.0.1-SNAPSHOT.jar app.jar

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]

