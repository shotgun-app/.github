# Social contract

### Team members (Project Group 4)
- Enrico Calderan, Jia Wei Chow, Lan Lebar, Núria Esquius Bau, Sven Ulcar

### Collaboration and communication

- We communicate through our Discord server, which has multiple channels for different topics.
- We have meetings on a weekly basis where we sync with each other. Everyone presents what they are working on, what they worked on, and if there are any blockers. The meetings are held on Discord server.
- Teacher assistant has access to parts of our Discord server
- Each sprint a new person is assigned to be the Scrum Master.
- Scrum master has to keep an overview on a sprint and who works on assigned items. They also suggest who should be assigned to a certain ticket.
- We all have varying working hours due to university work, so we don't define a fixed schedule. We expect all team members to check Discord at least once a day and respond/react to the messages within 24 hours.
- Announce planned absence at least 1 day in advance. Announce unplanned absence (illness, emergency) as soon as you reasonably can.
- Everone is expected to attend the weekly sync. If you cannot attend, post your update (working on / worked on / blockers) in Discord before the meeting.

### Definition of Done

An item is Done when all of the following criteria are met:
- All acceptance criteria in the issue are met
- Code is pushed on a feature branch and a pull request is opened and linked to the issue (`Closes #1`). That pull request must be merged into `main`
- The pull request is reviewed and approved by at least one other team member
- Tests cover the newly added features
- Manual testing is done by someone other than the author.
- Documentation is updated if the change affects project setup or usage
- The issue is closed and moved to Done on the Kanban card

### Reviewing and testing
- Technical roles are flexible. Anybody can work, reiview or test anything. We all review and test each other's work. These are not roles assigned to one person.
- The author never approves or merges their own pull request without review.
- The author moves the item into Review column and whoever is available reviews it. If nobody is available, the author can ask for a review in Discord.
- Reviewer checks: acceptance criteria, correctness, readability and tests.
- Reviewer and tester may be the same person.

### Deadlines

- If you see you will not finish an item on time, let the team know as early as possible, not on the deadline day.
- The Scrum Master and the assignee then decide together to either split the item, hand part of it over, or move it to the next sprint.
- If an item is blocked, move it back to TODO with a comment on the issue explaining why work cannot continue and when it can be resumed.
- If the same person repeatedly misses agreed work without communicating, the team raises it directly with them in the weekly sync. If it continues, we involve the teacher assistant.

### Disagreement and conflict

- We discuss disagreements in the relevant Discord channel or in the weekly sync
- We argue about the work and the trade-offs, not about the person
- In an event of a disagreement the Scrum Master mediates and ensures that we decide on the things democratically
- If discussion does not settle it, we vote. Majority wins. Once a decision is made, everybody must follow it.

### Tooling

- We use a Kanban board by GitHub projects. The first column (Backlog), holds our project/product backlog.
- We add items (user stories or tasks) as GitHub issues inside the GitHub repo, and open a pull request for each one.
- Linking pull requests to issue is done by typing Closes #1 into the PR description (#1 being issue number)
- We use the following columns on the Kanban board
    - Backlog: Product backlog items - from here we will pick the items for the next sprint
    - TODO: Ready to be picked up in this sprint. By the end of the sprint, all these items should be Done
    - In progress: This is actively being worked on
    - Review: Reviewing the pull request
    - Testing: Manual and automated testing. E2E tests need to written in this column
    - Done: Fully developed, merged, tested and deployed
- We have different issue templates: feature, bug, task (chore)
- An item is done when it meets the Definition of Done above

### Links

- Organization: [Shutgun App](https://github.com/shotgun-app)
    - [.github](https://github.com/shotgun-app/.github) (Shotgun README files)
    - [shotgun-api](https://github.com/shotgun-app/shotgun-api) (Shotgun Go API)
    - [shotgun-web](https://github.com/shotgun-app/shotgun-web) (Shotgun Vue web application)
- Project: [GitHub project](https://github.com/orgs/shotgun-app/projects/1)

### Agreement

All team members were present in the making and agree with the above social contract.
