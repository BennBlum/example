public abstract class BaseResponseHandler
{
    public virtual void GetResponse(ref List<AutoReplyResponseItem> responseList, AutoReplyResponseWriter response,
        AutoReplyInput autoReplyInput, IEnumerable<IntentType> intents, List<ReplyAction> actions, AutoReplyIntentResponseMap intentResponseMap)
    {
        List<IntentType> handleIntents = new List<IntentType>(intents);
        AutoReplyContext context = CreateContext(responseList, response, autoReplyInput, handleIntents, actions);

        if (!context.ResponseList.Any())
            return;

        ProcessResponse(context);
    }

    private AutoReplyContext CreateContext(List<AutoReplyResponseItem> responseList, AutoReplyResponseWriter response,
        AutoReplyInput autoReplyInput, List<IntentType> handleIntents, List<ReplyAction> actions)
    {
        return new AutoReplyContext
        {
            ResponseList = responseList.Where(intent => handleIntents.Contains(intent.Intent)),
            Patterns = null,
            Handled = false,
            PatternMethods = null,
            Response = response,
            Input = autoReplyInput,
            Actions = actions
        };
    }

    private void ProcessResponse(AutoReplyContext context)
    {
        Preprocessing(context);
        IdentifyPatterns(context);
        MapPatternToResponse(context);
        PreBuildResponse(context);
        BuildResponse(context);
        FinalizeResponse(context);
    }

    protected virtual void BuildResponse(AutoReplyContext context)
    {
        bool intentHandled = context.Handled;

        foreach (AutoReplyPattern key in context.Patterns.Keys.ToList())
        {
            if (context.PatternMethods.ContainsKey(key) && context.Patterns[key])
                context.PatternMethods[key](key, context);
        }
        context.Handled = intentHandled;
    }

    protected abstract void Preprocessing(AutoReplyContext context);
    protected abstract void IdentifyPatterns(AutoReplyContext context);
    protected abstract void MapPatternToResponse(AutoReplyContext context);
    protected abstract void PreBuildResponse(AutoReplyContext context);
    protected abstract void FinalizeResponse(AutoReplyContext context);
}