# SOP Authoring Guide

This guide explains how to create YAML-based Standard Operating Procedures (SOPs) for the SOP Automation Dashboard.

## Required Fields

Every SOP definition must include:

| Field | Description |
|-------|-------------|
| `name` | Human-readable SOP name |
| `entity` | Target entity: `mighty_house_inc`, `dsaic`, or `computer_store` |
| `triggers` | List of events that trigger the SOP |
| `steps` | List of steps to execute |

## Step Types

### Content & Social
- **`social_post`** - Post to social media platforms
- **`content_generate`** - Generate content using AI

### CRM Integration
- **`zoho_create_record`** - Create a record in Zoho CRM
- **`zoho_update_record`** - Update an existing record
- **`zoho_search`** - Search for records

### Flow Control
- **`approval`** - Human approval checkpoint
- **`condition`** - Branch based on conditions
- **`delay`** - Wait for time or condition
- **`loop`** - Iterate over records

### External
- **`webhook`** - Call external APIs
- **`cross_entity_trigger`** - Trigger SOP in another entity

## Variables

Use `{{variable}}` syntax to reference dynamic values:

```yaml
message: "Welcome {{customer_name}} to our team!"
```

Context variables available:
- `{{context.entity}}` - Current entity
- `{{context.execution_id}}` - Execution ID
- `{{context.started_at}}` - Start timestamp

## Minimal Example

```yaml
name: "Welcome New Customer"
entity: "computer_store"
description: "Send welcome message to new customers"

triggers:
  - type: manual
    label: "Run Welcome Sequence"
  - type: zoho_webhook
    module: Contacts
    event: create

steps:
  - id: post_welcome
    type: social_post
    name: "Post Welcome Message"
    config:
      platform: discord
      message: "🎮 Welcome {{customer_name}} to the gaming family!"
      
  - id: create_record
    type: zoho_create_record
    name: "Log in CRM"
    config:
      module: Contacts
      fields:
        Contact_Name: "{{customer_name}}"
        Lead_Source: "Walk-in"
        
  - id: wait_24h
    type: delay
    name: "Wait 24 hours"
    config:
      duration: "24h"
      
  - id: followup
    type: social_post
    name: "Followup Message"
    config:
      platform: discord
      message: "Hope you're enjoying your first day! Any questions?"
```

## Complete Example with Approval

```yaml
name: "Content Review Pipeline"
entity: "dsaic"
description: "AI-generated content with human approval"

triggers:
  - type: manual
    label: "Generate Content"

steps:
  - id: generate
    type: content_generate
    name: "Generate Draft"
    config:
      topic: "{{topic}}"
      platform: twitter
      
  - id: review
    type: approval
    name: "Human Review"
    config:
      approvers:
        - marketing-team
      timeout: "48h"
      
  - id: check_approval
    type: condition
    name: "Check if Approved"
    config:
      condition: "{{review.status}} == 'approved'"
      on_true:
        - id: publish
          type: social_post
          name: "Publish Content"
          config:
            platform: twitter
            message: "{{generate.content}}"
      on_false:
        - id: notify_rejection
          type: webhook
          name: "Notify Team"
          config:
            url: "https://slack.webhook.url"
            payload:
              text: "Content rejected: {{review.reason}}"
```

## File Locations

SOPs are stored in `sops/<entity>/` directories:

```
sops/
├── mighty_house_inc/
│   ├── contract_win.yaml
│   └── rfp_response.yaml
├── dsaic/
│   ├── product_launch.yaml
│   └── feature_release.yaml
└── computer_store/
    ├── tournament_event.yaml
    └── repair_intake.yaml
```

## Validation

Run validation before deploying:

```bash
python -m src.sop.engine validate sops/
```

Or test with dry-run:

```bash
curl -X POST http://localhost:8080/api/sop/computer_store/tournament_event/trigger?dry_run=true
```

## Dashboard Integration

- View SOPs: `http://localhost:8080/entity/{entity_id}`
- Trigger manually: Click "Run" button on SOP detail page
- Edit inline: `http://localhost:8080/sop/{entity_id}/{sop_id}/edit`
- View execution history: `http://localhost:8080/history`
