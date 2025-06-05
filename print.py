from langgraph.types import Command


def print_event(event, graph, config):
   
    quene = [event]
    while quene:
        current_event = quene.pop(0)
        # If interrupt, print approval prompt and run resumed events
        if "__interrupt__" in current_event:
            print("================================== Interrupt ==================================")
            print("Pending Executions!")
            print(graph.get_state(config).next)
            human_reply = input("Approve the tool call? (approve/reject): ").strip().lower()
            resume_cmd = Command(resume={"action": human_reply})
            # Stream out resumed messages and print them
            # 把 resumed_event 一個一個加到 queue，後面再處理
            for resumed_event in graph.stream(resume_cmd, config=config, stream_mode="values"):
                quene.append(resumed_event)
            continue

        if isinstance(current_event, dict) and "messages" in current_event:
            msg = current_event["messages"][-1]
            msg.pretty_print()
            print("")
        else:
            print(">>> Event without 'messages':", current_event)

