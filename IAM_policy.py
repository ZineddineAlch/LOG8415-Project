import boto3

IAM_RESOURCE = boto3.resource('iam')

policies = IAM_RESOURCE.policies.filter(
    Scope='AWS',
    PolicyUsageFilter='PermissionsPolicy',
    PathPrefix='/service-role/'
)

print('Search results:')

for policy in policies:
    print(f'  - {policy.policy_name}')