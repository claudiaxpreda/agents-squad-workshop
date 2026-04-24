```mermaid
graph LR
    %% Set the Dark-Friendly Colors
    classDef intake fill:#1f2937,stroke:#7dd3fc,stroke-width:2px,color:#dbeafe;
    classDef schedule fill:#111827,stroke:#86efac,stroke-width:2px,color:#d9f99d;
    classDef funky fill:#0f172a,stroke:#c4b5fd,stroke-width:2px,color:#e0f2fe;
    classDef file fill:#0f172a,stroke:#94a3b8,stroke-dasharray: 5 5,color:#f8fafc;

    %% The Flow
    Input([📄 messy_agenda.txt]) --> Agent1[🔍 Intake Agent]
    Agent1 -->|Clean Tasks| Agent2[📅 Scheduler Agent]
    Agent2 -->|Intermediate Table| Agent3[✨ Funky Agent]
    Agent3 --> Output([🌿 final_schedule.md])

    %% Assign Colors
    class Input,Output file;
    class Agent1 intake;
    class Agent2 schedule;
    class Agent3 funky;

    subgraph "Your Multi-Agent Team"
    Agent1
    Agent2
    Agent3
    end

```