#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run all tests with coverage report
"""

import os
import sys
import pytest
import coverage

def main():
    """Run all tests with coverage"""
    # Start coverage
    cov = coverage.Coverage(
        branch=True,
        source=["app"],
        omit=[
            "*/tests/*",
            "*/migrations/*",
            "*/__init__.py",
        ]
    )
    cov.start()

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add parent directory to path
    sys.path.append(os.path.dirname(current_dir))
    
    # Run tests with pytest
    test_args = [
        "--verbose",
        "--color=yes",
        "-s",
        current_dir
    ]
    
    result = pytest.main(test_args)
    
    # Stop coverage and generate report
    cov.stop()
    cov.save()
    
    print("\nCoverage Report:")
    cov.report()
    
    # Generate HTML report
    html_dir = os.path.join(current_dir, "htmlcov")
    cov.html_report(directory=html_dir)
    print(f"\nHTML coverage report generated in: {html_dir}")
    
    return result

if __name__ == "__main__":
    sys.exit(main()) 