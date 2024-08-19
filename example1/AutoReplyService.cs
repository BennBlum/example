
public interface IEnquiryParser
{
    List<AutoReplyResponseItem> ParseEnquiry(AutoReplyInput input, string country);
}

public interface IReplyGenerator
{
    AutoReplyOutput GenerateReply(AutoReplyInput input, List<AutoReplyResponseItem> responseItems);
}

public class EnquiryParser : IEnquiryParser
{
    private readonly NlpService _nlpService;

    public EnquiryParser(NlpService nlpService)
    {
        _nlpService = nlpService;
    }

    public List<AutoReplyResponseItem> ParseEnquiry(AutoReplyInput input, string country)
    {
        return _nlpService.ParseEnquiry(input, country).ToList();
    }
}

public class ReplyGenerator : IReplyGenerator
{
    private readonly List<BaseResponseHandler> _registeredHandlers;

    public ReplyGenerator(List<BaseResponseHandler> registeredHandlers)
    {
        _registeredHandlers = registeredHandlers;
    }

    public AutoReplyOutput GenerateReply(AutoReplyInput input, List<AutoReplyResponseItem> responseItems)

        foreach (BaseResponseHandler handler in _registeredHandlers)
        {
            try
            {

                if (intents.ContainsKey(handler.GetType()))
                    handler.GetResponse(ref responseDictionary, responseWriter, AutoReplyInput, intents[handler.GetType()], actions, AutoReplyIntentResponseMap);
            }
           catch (Exception ex)
            {
                Console.WriteLine($"Error occurred while processing handler: {ex.Message}");
            }            
        }
        return new AutoReplyOutput(responseDictionary);
    }
}

public class AutoReplyService
{
    private readonly IEnquiryParser _enquiryParser;
    private readonly IReplyGenerator _replyGenerator;
    private readonly Dictionary<Type, List<IntentType>> _intents;

    public AutoReplyService(IEnquiryParser enquiryParser, IReplyGenerator replyGenerator, Dictionary<Type, List<IntentType>> intents)
    {
        _enquiryParser = enquiryParser;
        _replyGenerator = replyGenerator;
        _intents = intents;
    }

    public AutoReplyOutput GetReply(AutoReplyInput input)
    {
        var responseItems = _enquiryParser.ParseEnquiry(input, input.Country);
        return _replyGenerator.GenerateReply(input, responseItems);
    }

    public List<BaseResponseHandler> RegisterHandlers(TextEncoder encoder)
    {
        var registeredHandlers = new List<BaseResponseHandler>();

        foreach (var intent in _intents.Keys)
        {
            var handler = (BaseResponseHandler)Activator.CreateInstance(intent, encoder);
            registeredHandlers.Add(handler);
        }

        return registeredHandlers;
    }
}