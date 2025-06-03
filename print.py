from langgraph.types import Command


def print_event(event, graph, config):
    # If interrupt, print approval prompt and run resumed events
    if "__interrupt__" in event:
        print("================================== Interrupt ==================================")
        print("Pending Executions!")
        print(graph.get_state(config).next)
        human_reply = input("Approve the tool call? (approve/reject): ").strip().lower()
        resume_cmd = Command(resume={"action": human_reply})
        # Stream out resumed messages and print them
        for resumed_event in graph.stream(resume_cmd, config=config, stream_mode="values"):
            msg = resumed_event["messages"][-1]
            msg.pretty_print()
            print("")
    else:
        # Normal message: print the last user/assistant/tool message
        msg = event["messages"][-1]
        msg.pretty_print()
        print("")

