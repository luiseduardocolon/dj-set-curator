"""
Temporal Workflow - Hour 6 Hello World
Basic workflow to verify Temporal is working
"""
from datetime import timedelta
from temporalio import workflow

@workflow.defn
class HelloWorkflow:
    """
    Simple hello world workflow
    Demonstrates basic Temporal workflow structure
    """
    
    @workflow.run
    async def run(self, name: str) -> str:
        """
        Main workflow method
        
        Args:
            name: Name to greet
            
        Returns:
            Greeting message
        """
        workflow.logger.info(f"HelloWorkflow started for: {name}")
        
        greeting = f"Hello, {name}! Welcome to Temporal DJ Set Curator!"
        
        workflow.logger.info(f"HelloWorkflow completed: {greeting}")
        
        return greeting

# Workflow will be registered by the worker

