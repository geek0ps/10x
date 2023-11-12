# Linux Util Scripts


## System Health Check

```sh
#!/bin/bash

# Thresholds
CPU_THRESHOLD=80
DISK_THRESHOLD=90
MEM_THRESHOLD=80

# Check CPU usage
cpu_usage=$(top -bn1 | grep load | awk '{printf "%.2f\n", $(NF-2)}')
if [ $(echo "$cpu_usage > $CPU_THRESHOLD" | bc) -ne 0 ]; then
    echo "High CPU usage: $cpu_usage %"
fi

# Check Disk usage
disk_usage=$(df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }')
while read -r line; do
    use_percent=$(echo $line | awk '{ print $1}' | cut -d'%' -f1)
    partition=$(echo $line | awk '{ print $2 }')
    if [ $use_percent -ge $DISK_THRESHOLD ]; then
        echo "High Disk usage on $partition ($use_percent%)"
    fi
done <<< "$disk_usage"

# Check Memory usage
mem_usage=$(free -m | awk 'NR==2{printf "%.2f", $3*100/$2 }')
if [ $(echo "$mem_usage > $MEM_THRESHOLD" | bc) -ne 0 ]; then
    echo "High Memory usage: $mem_usage %"
fi

```



## Backup Script


```sh

#!/bin/bash

BACKUP_SRC="/home/user/data"
BACKUP_DEST="/mnt/backup"
REMOTE_HOST="backup@example.com"
REMOTE_DIR="/remote/backup/dir"

tar czf "${BACKUP_DEST}/backup-$(date +%Y%m%d%H%M%S).tgz" "$BACKUP_SRC"
scp "${BACKUP_DEST}/backup-*.tgz" $REMOTE_HOST:"$REMOTE_DIR"


```



## Clean Temporary files

```sh
#!/bin/bash

TEMP_DIRS=("/tmp" "/var/tmp")
MAX_AGE=7  # days

find "${TEMP_DIRS[@]}" -type f -mtime +$MAX_AGE -exec rm -f {} \;

```




## Batch Image Optimization

```sh
#!/bin/bash

IMAGE_DIR="/path/to/images"
MAX_WIDTH=800
MAX_HEIGHT=600

for img in "$IMAGE_DIR"/*.jpg; do
    convert "$img" -resize "${MAX_WIDTH}x${MAX_HEIGHT}\>" "$img"
done


```


## DB Backup


```sh

#!/bin/bash

DB_NAME="your_database"
BACKUP_DIR="/path/to/backup/dir"
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}-$(date +%Y%m%d%H%M%S).sql"

mysqldump -u [username] -p[password] $DB_NAME > $BACKUP_FILE


```


## User account audit script

```sh
#!/bin/bash

INACTIVE_THRESHOLD=90  # days
TODAY=$(date +%s)

lastlog | grep -v Never | while read -r line; do
    username=$(echo $line | awk '{print $1}')
    last_login=$(echo $line | awk '{print $4, $5, $6}')
    last_login_seconds=$(date -d "$last_login" +%s)
    inactive_days=$(( ($TODAY - $last_login_seconds) / 86400 ))
    if [ $inactive_days -ge $INACTIVE_THRESHOLD ]; then
        echo "User $username has been inactive for $inactive_days days."
    fi
done

```



## Disk space usage Alert

```sh
#!/bin/bash

THRESHOLD=90  # Percentage
EMAIL="admin@example.com"

df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }' | while read output;
do
  usep=$(echo $output | awk '{ print $1}' | cut -d'%' -f1)
  partition=$(echo $output | awk '{ print $2 }')
  if [ $usep -ge $THRESHOLD ]; then
    echo "Running out of space \"$partition ($usep%)\" on $(hostname) as on $(date)" |
    mail -s "Alert: Almost out of disk space $usep%" $EMAIL
  fi
done

```

## SSL / TLS Cipher test suite


```sh

#!/bin/bash

SERVER="yourserver.com"
PORT=443
EMAIL="admin@example.com"

if ! nmap --script ssl-enum-ciphers -p $PORT $SERVER | grep -q "strong encryption"; then
    echo "Weak SSL/TLS ciphers detected on $SERVER:$PORT" | mail -s "SSL/TLS Cipher Alert" $EMAIL
fi

```

## Automated data purging script

```sh
#!/bin/bash

DB_HOST="localhost"
DB_USER="user"
DB_PASSWORD="password"
DB_NAME="your_db"
PURGE_OLDER_THAN="365 DAY"  # Example for 1 year

mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME -e "DELETE FROM your_table WHERE date_column < NOW() - INTERVAL $PURGE_OLDER_THAN;"


```



## Resize CPU resource on aws or azure


```sh

#!/bin/bash
fetch_cpu_usage_from_monitoring_service() {
    cloud_provider=$1
    server_id=$2

    if [ "$cloud_provider" == "aws" ]; then
        # AWS logic (same as before)
        cpu_usage=$(aws cloudwatch get-metric-statistics --namespace AWS/EC2 \
                    --metric-name CPUUtilization \
                    --dimensions Name=InstanceId,Value=$server_id \
                    --statistics Average \
                    --period 600 \
                    --start-time $(date --date='10 minutes ago' --iso-8601=seconds) \
                    --end-time $(date --iso-8601=seconds) \
                    --query 'Datapoints[0].Average' \
                    --output text)
    elif [ "$cloud_provider" == "azure" ]; then
        # Azure logic using REST API
        RESOURCE_GROUP="yourResourceGroup"
        VM_NAME="yourVMName"
        SUBSCRIPTION_ID="yourSubscriptionId"
        TENANT_ID="yourTenantId"
        CLIENT_ID="yourClientId"
        CLIENT_SECRET="yourClientSecret"

        # Get Azure Access Token
        access_token=$(curl -X POST -d "grant_type=client_credentials&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET&resource=https://management.azure.com/" \
                       -H "Content-Type: application/x-www-form-urlencoded" \
                       "https://login.microsoftonline.com/$TENANT_ID/oauth2/token" | jq -r '.access_token')

        # Define time range
        end_time=$(date --utc +%Y-%m-%dT%H:%MZ)
        start_time=$(date --utc --date='10 minutes ago' +%Y-%m-%dT%H:%MZ)

        # Azure Monitor REST API endpoint
        metric_url="https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Compute/virtualMachines/$VM_NAME/providers/microsoft.insights/metrics?api-version=2018-01-01&metricnames=Percentage%20CPU&timespan=${start_time}/${end_time}&interval=PT1M&aggregation=average"

        # Fetch CPU usage metric
        cpu_usage=$(curl -s -X GET -H "Authorization: Bearer $access_token" -H "Content-Type: application/json" "$metric_url" | jq -r '.value[0].timeseries[0].data[-1].average')
    fi

    echo $cpu_usage
}

check_cpu_usage_and_resize() {
    cloud_provider=$1
    server_id=$2

    # Define thresholds
    HIGH_THRESHOLD=80
    LOW_THRESHOLD=20

    # Define instance types for AWS and Azure
    AWS_HIGH_TYPE="m5.large"
    AWS_LOW_TYPE="t2.small"
    AZURE_HIGH_TYPE="Standard_B2s"
    AZURE_LOW_TYPE="Standard_B1s"

    cpu_usage=$(fetch_cpu_usage_from_monitoring_service $cloud_provider $server_id)

    if [ "$cpu_usage" -ge "$HIGH_THRESHOLD" ]; then
        if [ "$cloud_provider" == "aws" ]; then
            aws ec2 modify-instance-attribute --instance-id $server_id --instance-type $AWS_HIGH_TYPE
            echo "AWS instance $server_id resized to $AWS_HIGH_TYPE due to high CPU usage."
        elif [ "$cloud_provider" == "azure" ]; then
            az vm resize --resource-group YourResourceGroup --name $server_id --size $AZURE_HIGH_TYPE
            echo "Azure VM $server_id resized to $AZURE_HIGH_TYPE due to high CPU usage."
        fi
    elif [ "$cpu_usage" -le "$LOW_THRESHOLD" ]; then
        if [ "$cloud_provider" == "aws" ]; then
            aws ec2 modify-instance-attribute --instance-id $server_id --instance-type $AWS_LOW_TYPE
            echo "AWS instance $server_id resized to $AWS_LOW_TYPE due to low CPU usage."
        elif [ "$cloud_provider" == "azure" ]; then
            az vm resize --resource-group YourResourceGroup --name $server_id --size $AZURE_LOW_TYPE
            echo "Azure VM $server_id resized to $AZURE_LOW_TYPE due to low CPU usage."
        fi
    fi
}


check_cpu_usage_and_resize "aws" "i-1234567890abcdef0"

check_cpu_usage_and_resize "azure" "yourAzureVmName"

```