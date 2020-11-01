version: '3.7'
services:
  web:
    environment:
      DEPLOY_ENV: ${env}
      GH_API_TOKEN: ${gh_api_token}
      GH_REPO_NAME: ${gh_repo_name}
      GH_OWNER: ${gh_owner}
      GH_PR_THRESH: ${gh_pr_thresh}
      SLACK_HOOK: ${slack_hook}
      GH_PR_INTERVAL: ${gh_pr_interval}
    deploy:
      placement:
        constraints: [node.role==worker]
      replicas: ${replicas}
      resources:
        limits:
          cpus: '0.5'
          memory: 200m
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 300s          
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
        failure_action: rollback
    image: bowens/github-pr-slack-monitor:${tag}
    networks:
      - github-net
networks:
  github-net:
    driver: overlay