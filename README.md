# Python API with Azure Cosmos DB

## Requirements

- **Platform**: x86-64, Linux/WSL
- **Programming Language**: [Python 3](https://www.python.org/downloads/)
- **Terraform**: For provisioning [Azure resources](infra/terraform.tf)
- **Azure Account**: Access to [Azure Subscription](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account)

## Allocate resources

The script [up](up.sh) provisions Azure resources by applying our [Terraform script](infra/terraform.tf).


## Running API
```bash
python -m uvicorn main:app --reload
```


## Deallocate resources

The script [down](down.sh) removes provisioned Azure resources running **terraform destroy**.

## Postman collection
A collection of sample request has been included under the [postman](postman) directory.