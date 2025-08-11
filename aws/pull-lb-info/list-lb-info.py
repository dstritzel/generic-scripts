#!/usr/bin/env python3
"""
AWS Load Balancer Information Retriever

This script retrieves detailed information about all Elastic Load Balancers (ELBv2) 
in your AWS account, including their associated listeners, and outputs the data in JSON format.

Usage:
    python list-lb-info.py                    # Output to stdout
    python list-lb-info.py -o output.json     # Output to file
    python list-lb-info.py --help             # Show help

Requirements:
- AWS credentials configured (via AWS CLI, environment variables, or IAM role)
- IAM permissions: elasticloadbalancing:DescribeLoadBalancers, elasticloadbalancing:DescribeListeners
"""

import argparse
import boto3
import json
import sys
from botocore.exceptions import ClientError, NoCredentialsError


def get_load_balancer_info():
    """
    Retrieve information about all load balancers and their listeners.
    
    Returns:
        list: A list of dictionaries containing load balancer information with listeners
    """
    try:
        # Initialize ELBv2 client
        elb_client = boto3.client('elbv2')
        
        # Get all load balancers
        response = elb_client.describe_load_balancers()
        load_balancers = response['LoadBalancers']
        
        # Process each load balancer
        enhanced_load_balancers = []
        
        for load_balancer in load_balancers:
            # Create a copy of the load balancer data
            lb_data = dict(load_balancer)
            
            # Clear CreatedTime as it's not JSON serializable (datetime object)
            lb_data['CreatedTime'] = ""
            
            # Initialize listeners list
            lb_data['Listeners'] = []
            
            # Get listeners for this load balancer
            try:
                listeners_response = elb_client.describe_listeners(
                    LoadBalancerArn=load_balancer['LoadBalancerArn']
                )
                
                # Add all listeners to the load balancer data
                for listener in listeners_response['Listeners']:
                    lb_data['Listeners'].append(listener)
                    
            except ClientError as e:
                print(f"Warning: Could not retrieve listeners for {load_balancer['LoadBalancerName']}: {e}", 
                      file=sys.stderr)
                
            enhanced_load_balancers.append(lb_data)
            
        return enhanced_load_balancers
        
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your AWS credentials.", 
              file=sys.stderr)
        sys.exit(1)
        
    except ClientError as e:
        print(f"Error: AWS API call failed: {e}", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Retrieve AWS Load Balancer information and output as JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Output to stdout
  %(prog)s -o loadbalancers.json     # Output to file
  %(prog)s --output lb_info.json     # Output to file (long form)
        """
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        metavar='FILE',
        help='Output JSON to specified file instead of stdout'
    )
    
    return parser.parse_args()


def main():
    """Main function to execute the load balancer information retrieval."""
    # Parse command line arguments
    args = parse_arguments()
    
    print("Retrieving load balancer information...", file=sys.stderr)
    
    # Get load balancer information
    load_balancer_data = get_load_balancer_info()
    
    # Convert to JSON
    json_output = json.dumps(load_balancer_data, indent=2, default=str)
    
    # Output to file or stdout
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f"Successfully wrote load balancer information to '{args.output}'", file=sys.stderr)
        except IOError as e:
            print(f"Error: Could not write to file '{args.output}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(json_output)
    
    print(f"Successfully retrieved information for {len(load_balancer_data)} load balancer(s).", 
          file=sys.stderr)


if __name__ == "__main__":
    main()
